from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalogo.models import Ejemplar, Obra
from gestionUsuarios.models import Socio
from prestamos.models import Prestamo


Usuario = get_user_model()


class PenalizacionesSocioTests(TestCase):
    def setUp(self):
        self.socio = self.crear_socio()

    def crear_socio(self, username="socio"):
        usuario = Usuario.objects.create_user(
            username=username,
            password="test-password",
            tipo=Usuario.TipoUsuario.SOCIO,
        )
        return Socio.objects.create(usuario=usuario)

    def crear_ejemplar(self):
        numero = Ejemplar.objects.count() + 1
        obra = Obra.objects.create(
            titulo=f"Obra de prueba {numero}",
            signatura=f"TEST-{numero}",
            tipo="LIBRO",
        )
        return Ejemplar.objects.create(obra=obra)

    def crear_prestamo(self, socio, fecha_fin):
        return Prestamo.objects.create(
            socio=socio,
            ejemplar=self.crear_ejemplar(),
            fechaFin=fecha_fin,
        )

    def crear_bibliotecario(self):
        return Usuario.objects.create_user(
            username="bibliotecario",
            password="test-password",
            tipo=Usuario.TipoUsuario.BIBLIOTECARIO,
        )

    def test_socio_nuevo_no_esta_penalizado(self):
        self.assertFalse(self.socio.esta_penalizado)
        self.assertEqual(
            self.socio.estado_penalizacion,
            Socio.EstadoPenalizacion.SIN_CASTIGO,
        )

    def test_prestamo_vencido_genera_penalizacion_indefinida(self):
        ayer = timezone.localdate() - timedelta(days=1)
        self.crear_prestamo(self.socio, ayer)

        self.assertTrue(self.socio.esta_penalizado)
        self.assertEqual(
            self.socio.estado_penalizacion,
            Socio.EstadoPenalizacion.INDEFINIDO,
        )
        self.assertIsNone(self.socio.fechaPenalizacion)

    def test_prestamo_que_vence_durante_castigo_temporal_lo_hace_indefinido(self):
        self.socio.estado_penalizacion = Socio.EstadoPenalizacion.TEMPORAL
        self.socio.fechaPenalizacion = timezone.localdate()
        self.socio.save()

        ayer = timezone.localdate() - timedelta(days=1)
        self.crear_prestamo(self.socio, ayer)

        self.assertTrue(self.socio.esta_penalizado)
        self.assertEqual(
            self.socio.estado_penalizacion,
            Socio.EstadoPenalizacion.INDEFINIDO,
        )
        self.assertIsNone(self.socio.fechaPenalizacion)

    @patch("prestamos.models.DIAS_CASTIGO", 2)
    def test_castigo_temporal_activo_sigue_bloqueando(self):
        self.socio.estado_penalizacion = Socio.EstadoPenalizacion.TEMPORAL
        self.socio.fechaPenalizacion = timezone.localdate() - timedelta(days=1)
        self.socio.save()

        self.assertTrue(self.socio.esta_penalizado)

    @patch("prestamos.models.DIAS_CASTIGO", 2)
    def test_al_acabar_castigo_temporal_se_limpia_el_estado(self):
        self.socio.estado_penalizacion = Socio.EstadoPenalizacion.TEMPORAL
        self.socio.fechaPenalizacion = timezone.localdate() - timedelta(days=2)
        self.socio.save()

        self.assertFalse(self.socio.esta_penalizado)
        self.assertEqual(
            self.socio.estado_penalizacion,
            Socio.EstadoPenalizacion.SIN_CASTIGO,
        )
        self.assertIsNone(self.socio.fechaPenalizacion)

    def test_devolver_el_ultimo_vencido_inicia_un_nuevo_castigo_temporal(self):
        bibliotecario = self.crear_bibliotecario()
        self.client.force_login(bibliotecario)

        ayer = timezone.localdate() - timedelta(days=1)
        primer_prestamo = self.crear_prestamo(self.socio, ayer)
        segundo_prestamo = self.crear_prestamo(self.socio, ayer)

        # Mientras quede otro préstamo vencido, el castigo sigue indefinido.
        respuesta = self.client.post(
            reverse(
                "prestamos:devolver_ejemplar",
                args=[primer_prestamo.pk],
            )
        )
        self.assertEqual(respuesta.status_code, 302)

        self.socio.refresh_from_db()
        self.assertEqual(
            self.socio.estado_penalizacion,
            Socio.EstadoPenalizacion.INDEFINIDO,
        )
        self.assertEqual(self.socio.numCaducados, 1)

        # Al devolver el último vencido tarde, empieza el temporal desde hoy.
        respuesta = self.client.post(
            reverse(
                "prestamos:devolver_ejemplar",
                args=[segundo_prestamo.pk],
            )
        )
        self.assertEqual(respuesta.status_code, 302)

        self.socio.refresh_from_db()
        self.assertEqual(
            self.socio.estado_penalizacion,
            Socio.EstadoPenalizacion.TEMPORAL,
        )
        self.assertEqual(self.socio.fechaPenalizacion, timezone.localdate())
        self.assertEqual(self.socio.numCaducados, 0)

    def test_no_se_puede_prestar_a_un_socio_penalizado(self):
        bibliotecario = self.crear_bibliotecario()
        self.client.force_login(bibliotecario)

        ayer = timezone.localdate() - timedelta(days=1)
        self.crear_prestamo(self.socio, ayer)
        ejemplar_nuevo = self.crear_ejemplar()

        respuesta = self.client.post(
            reverse(
                "prestamos:prestar_ejemplar",
                args=[ejemplar_nuevo.pk],
            ),
            {"socio": self.socio.pk},
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(
            Prestamo.objects.filter(ejemplar=ejemplar_nuevo).count(),
            0,
        )

    def test_se_puede_prestar_a_un_socio_sin_penalizacion(self):
        bibliotecario = self.crear_bibliotecario()
        self.client.force_login(bibliotecario)
        ejemplar = self.crear_ejemplar()

        respuesta = self.client.post(
            reverse(
                "prestamos:prestar_ejemplar",
                args=[ejemplar.pk],
            ),
            {"socio": self.socio.pk},
        )

        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(
            Prestamo.objects.filter(
                socio=self.socio,
                ejemplar=ejemplar,
            ).exists()
        )
        
    def test_devolucion_en_plazo_no_altera_castigo_temporal(self):
        bibliotecario = self.crear_bibliotecario()
        self.client.force_login(bibliotecario)

        self.socio.estado_penalizacion = Socio.EstadoPenalizacion.TEMPORAL
        self.socio.fechaPenalizacion = timezone.localdate()
        self.socio.save()

        manana = timezone.localdate() + timedelta(days=5)
        prestamo = self.crear_prestamo(self.socio, manana)

        respuesta = self.client.post(
            reverse("prestamos:devolver_ejemplar", args=[prestamo.pk])
        )
        self.assertEqual(respuesta.status_code, 302)

        self.socio.refresh_from_db()
        self.assertEqual(
            self.socio.estado_penalizacion,
            Socio.EstadoPenalizacion.TEMPORAL,
        )
        
    @patch("prestamos.models.DIAS_CASTIGO", 2)
    def test_devolver_vencido_con_castigo_temporal_previo_reinicia(self):
        bibliotecario = self.crear_bibliotecario()
        self.client.force_login(bibliotecario)

        self.socio.estado_penalizacion = Socio.EstadoPenalizacion.TEMPORAL
        self.socio.fechaPenalizacion = timezone.localdate() - timedelta(days=1)
        self.socio.save()

        ayer = timezone.localdate() - timedelta(days=1)
        prestamo = self.crear_prestamo(self.socio, ayer)

        respuesta = self.client.post(
            reverse("prestamos:devolver_ejemplar", args=[prestamo.pk])
        )
        self.assertEqual(respuesta.status_code, 302)

        self.socio.refresh_from_db()
        self.assertEqual(self.socio.fechaPenalizacion, timezone.localdate())