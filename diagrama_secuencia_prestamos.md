# Diagrama de secuencia: préstamos, caducidad y prórrogas

```drawio
<mxfile>
  <diagram id="rvEKF-NW0RdYvkNipNv9" name="Page-1">
    <mxGraphModel dx="4329" dy="2104" grid="1" gridSize="10" guides="1" tooltips="0" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-0" />
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-1" parent="1rj4Dn4LaAnzpcD3HqiI-0" />
        <UserObject label="" mermaidData="{&#xa;  &quot;data&quot;: &quot;sequenceDiagram\r\n    autonumber\r\n    actor B as Bibliotecario\r\n    actor S as Socio\r\n    participant V as Vista de préstamos\r\n    participant SM as Modelo Socio\r\n    participant PM as Modelo Prestamo\r\n    participant DB as Base de datos\r\n\r\n    rect rgb(235, 245, 255)\r\n        Note over B,DB: Alta de préstamo (una solicitud por ejemplar)\r\n        B-&gt;&gt;V: POST prestar_ejemplar(ejemplar, socio)\r\n        V-&gt;&gt;DB: Comprobar obra prestable y ejemplar disponible\r\n        alt Obra no prestable o ejemplar ocupado\r\n            V--&gt;&gt;B: Rechazo; no se crea préstamo\r\n        else Ejemplar prestable y disponible\r\n            V-&gt;&gt;SM: consultar esta_penalizado\r\n            SM-&gt;&gt;DB: Contar préstamos con fechaDevolucion nula y fechaFin &lt; hoy\r\n            alt Existe al menos un vencido\r\n                SM-&gt;&gt;DB: Guardar estado indefinido y fechaPenalizacion nula\r\n                SM--&gt;&gt;V: Penalizado\r\n                V--&gt;&gt;B: Rechazar préstamo\r\n            else No hay vencidos\r\n                alt Castigo temporal vigente\r\n                    SM--&gt;&gt;V: Penalizado\r\n                    V--&gt;&gt;B: Rechazar préstamo\r\n                else Castigo temporal expirado\r\n                    SM-&gt;&gt;DB: Limpiar estado temporal\r\n                    SM--&gt;&gt;V: No penalizado\r\n                else Sin castigo\r\n                    SM--&gt;&gt;V: No penalizado\r\n                end\r\n                V-&gt;&gt;DB: Contar préstamos activos del tipo de obra\r\n                alt Límite del tipo alcanzado\r\n                    V--&gt;&gt;B: Rechazar préstamo\r\n                else Dentro del límite\r\n                    V-&gt;&gt;PM: Crear préstamo del ejemplar\r\n                    Note over PM: fechaFin = hoy + DIAS_PRESTAMO&lt;br/&gt;prorrogasRestantes = PRORROGAS_INICIALES\r\n                    PM-&gt;&gt;DB: Guardar préstamo activo\r\n                    V--&gt;&gt;B: Préstamo registrado\r\n                end\r\n            end\r\n        end\r\n    end\r\n\r\n    loop Para cada ejemplar prestado, con vencimiento y prórrogas independientes\r\n        opt El socio consulta la opción de prorrogar (GET)\r\n            S-&gt;&gt;V: GET prorrogar_prestamo(id)\r\n            V-&gt;&gt;DB: Obtener préstamo, socio y propietario\r\n            alt Sin permiso, ya devuelto o fechaFin &lt; hoy\r\n                V--&gt;&gt;S: Rechazo; no modificar préstamo\r\n            else Propietario, bibliotecario o administrador; activo y no vencido\r\n                V--&gt;&gt;S: Mostrar confirmación y días configurados\r\n            end\r\n        end\r\n\r\n        opt El socio confirma la prórroga (POST)\r\n            S-&gt;&gt;V: POST prorrogar_prestamo(id)\r\n            V-&gt;&gt;DB: Obtener préstamo y comprobar permiso\r\n            alt Sin permiso\r\n                V--&gt;&gt;S: Rechazar\r\n            else Tiene permiso\r\n                V-&gt;&gt;PM: Comprobar fechaDevolucion y fechaFin\r\n                alt Ya devuelto\r\n                    V--&gt;&gt;S: Rechazar; préstamo ya devuelto\r\n                else fechaFin &lt; hoy\r\n                    V--&gt;&gt;S: Rechazar; debe devolver el vencido\r\n                else Activo y no vencido\r\n                    V-&gt;&gt;SM: consultar esta_penalizado\r\n                    SM-&gt;&gt;DB: Recalcular vencidos activos del socio\r\n                    alt Socio penalizado\r\n                        SM--&gt;&gt;V: Penalizado\r\n                        V--&gt;&gt;S: Rechazar prórroga\r\n                    else Socio no penalizado\r\n                        V-&gt;&gt;PM: Comprobar prorrogasRestantes\r\n                        alt No quedan prórrogas\r\n                            V--&gt;&gt;S: Rechazar; no quedan prórrogas\r\n                        else Quedan prórrogas\r\n                            V-&gt;&gt;PM: Aplicar prórroga\r\n                            Note over PM: fechaFin += DIAS_PRORROGA&lt;br/&gt;fechaProrroga = hoy&lt;br/&gt;prorrogasRestantes -= 1\r\n                            PM-&gt;&gt;DB: Guardar fechas y contador\r\n                            V--&gt;&gt;S: Confirmar nueva fecha de devolución\r\n                        end\r\n                    end\r\n                end\r\n            end\r\n        end\r\n\r\n        Note over S,DB: Al pasar la fecha fin, el préstamo solo cuenta como vencido si no se ha devuelto.&lt;br/&gt;La comprobación es fechaFin &lt; hoy; no hay transición automática por un proceso en segundo plano.\r\n\r\n        opt Se consulta la penalización o se intenta un nuevo préstamo\r\n            V-&gt;&gt;SM: consultar esta_penalizado\r\n            SM-&gt;&gt;DB: Contar todos los préstamos vencidos sin devolver\r\n            alt Uno o más vencidos\r\n                SM-&gt;&gt;DB: Guardar estado indefinido\r\n                SM--&gt;&gt;V: Penalizado; numCaducados = cantidad de vencidos\r\n            else No hay vencidos y castigo temporal expirado\r\n                SM-&gt;&gt;DB: Limpiar castigo temporal\r\n                SM--&gt;&gt;V: No penalizado\r\n            else No hay vencidos y castigo vigente\r\n                SM--&gt;&gt;V: Penalizado temporalmente\r\n            else No hay vencidos ni castigo vigente\r\n                SM--&gt;&gt;V: Sin castigo\r\n            end\r\n        end\r\n\r\n        opt Bibliotecario registra una devolución\r\n            B-&gt;&gt;V: POST devolver_ejemplar(id)\r\n            V-&gt;&gt;PM: Comprobar que sigue activo\r\n            alt Ya devuelto\r\n                V--&gt;&gt;B: Informar; sin cambios\r\n            else Activo\r\n                V-&gt;&gt;DB: Guardar fechaDevolucion = hoy\r\n                V-&gt;&gt;PM: Comparar hoy con fechaFin\r\n                alt Devolución en plazo (hoy &lt;= fechaFin)\r\n                    Note over V,SM: No cambia el estado de penalización\r\n                    V--&gt;&gt;B: Devolución registrada\r\n                else Devolución tardía (hoy &gt; fechaFin)\r\n                    V-&gt;&gt;SM: Consultar numCaducados tras guardar devolución\r\n                    SM-&gt;&gt;DB: Contar otros préstamos vencidos aún sin devolver\r\n                    alt Quedan otros vencidos (numCaducados &gt; 0)\r\n                        V-&gt;&gt;DB: Mantener/guardar penalización indefinida\r\n                        V--&gt;&gt;B: Devolución registrada; persiste la penalización indefinida\r\n                    else Era el último vencido (numCaducados = 0)\r\n                        V-&gt;&gt;DB: Guardar castigo temporal con fechaPenalizacion = hoy\r\n                        V--&gt;&gt;B: Devolución registrada; comienza o se reinicia el castigo temporal\r\n                    end\r\n                end\r\n            end\r\n        end\r\n    end&quot;,&#xa;  &quot;config&quot;: null&#xa;}" id="PjRlD1XJtcLBet5u5arM-0">
          <mxCell connectable="0" parent="1rj4Dn4LaAnzpcD3HqiI-1" style="group;transparentBounds=1;editIcon=1;lockedGroup=0;groupPadding=10;" vertex="1">
            <mxGeometry as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-2" parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;rounded=0;strokeColor=none;fillColor=#ebf5ff;fillOpacity=100;pointerEvents=0;fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" value="" vertex="1">
          <mxGeometry height="1404" width="1586" x="45" y="85" as="geometry" />
        </mxCell>
        <UserObject label="Bibliotecario" mermaidId="n:B" mermaidBaseStyle="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);participant=seqActorStick;verticalAlign=bottom;align=center;spacingBottom=4;size=90;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Bibliotecario" id="1rj4Dn4LaAnzpcD3HqiI-3">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);participant=seqActorStick;verticalAlign=bottom;align=center;spacingBottom=4;size=90;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="4934" width="150" x="10" y="10" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Socio" mermaidId="n:S" mermaidBaseStyle="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);participant=seqActorStick;verticalAlign=bottom;align=center;spacingBottom=4;size=90;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Socio" id="1rj4Dn4LaAnzpcD3HqiI-4">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);participant=seqActorStick;verticalAlign=bottom;align=center;spacingBottom=4;size=90;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="4934" width="150" x="270" y="10" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Vista de préstamos" mermaidId="n:V" mermaidBaseStyle="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);size=65;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Vista de préstamos" id="1rj4Dn4LaAnzpcD3HqiI-5">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);size=65;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="4909" width="150" x="614" y="10" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Modelo Socio" mermaidId="n:SM" mermaidBaseStyle="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);size=65;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Modelo Socio" id="1rj4Dn4LaAnzpcD3HqiI-6">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);size=65;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="4909" width="150" x="1028" y="10" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Modelo Prestamo" mermaidId="n:PM" mermaidBaseStyle="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);size=65;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Modelo Prestamo" id="1rj4Dn4LaAnzpcD3HqiI-7">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);size=65;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="4909" width="150" x="1272" y="10" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Base de datos" mermaidId="n:DB" mermaidBaseStyle="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);size=65;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Base de datos" id="1rj4Dn4LaAnzpcD3HqiI-8">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;container=1;dropTarget=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;newEdgeStyle={&quot;edgeStyle&quot;:&quot;sequenceEdgeStyle&quot;,&quot;libavoidRouting&quot;:0,&quot;curved&quot;:0,&quot;rounded&quot;:0};lifelineDashed=0;strokeWidth=2;rounded=1;absoluteArcSize=1;arcSize=6;lifelineColor=light-dark(#9370DB,#cccccc);size=65;lifelineMirror=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="4909" width="150" x="1516" y="10" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="alt" mermaidId="n:f1" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-9">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="1235" width="1566" x="55" y="244" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-10" parent="1rj4Dn4LaAnzpcD3HqiI-9" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Obra no prestable o ejemplar ocupado]" vertex="1">
          <mxGeometry height="16" width="1512" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-11" parent="1rj4Dn4LaAnzpcD3HqiI-9" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1566" y="96" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-12" parent="1rj4Dn4LaAnzpcD3HqiI-9" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Ejemplar prestable y disponible]" vertex="1">
          <mxGeometry height="16" width="1566" y="98" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f2" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-13">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="997" width="1546" x="65" y="472" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-14" parent="1rj4Dn4LaAnzpcD3HqiI-13" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Existe al menos un vencido]" vertex="1">
          <mxGeometry height="16" width="1492" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-15" parent="1rj4Dn4LaAnzpcD3HqiI-13" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1546" y="188" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-16" parent="1rj4Dn4LaAnzpcD3HqiI-13" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[No hay vencidos]" vertex="1">
          <mxGeometry height="16" width="1546" y="190" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f3" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-17">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="365" width="1526" x="75" y="700" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-18" parent="1rj4Dn4LaAnzpcD3HqiI-17" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Castigo temporal vigente]" vertex="1">
          <mxGeometry height="16" width="1472" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-19" parent="1rj4Dn4LaAnzpcD3HqiI-17" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1526" y="142" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-20" parent="1rj4Dn4LaAnzpcD3HqiI-17" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Castigo temporal expirado]" vertex="1">
          <mxGeometry height="16" width="1526" y="144" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-21" parent="1rj4Dn4LaAnzpcD3HqiI-17" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1526" y="279" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-22" parent="1rj4Dn4LaAnzpcD3HqiI-17" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Sin castigo]" vertex="1">
          <mxGeometry height="16" width="1526" y="281" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f4" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-23">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="338" width="1526" x="75" y="1121" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-24" parent="1rj4Dn4LaAnzpcD3HqiI-23" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Límite del tipo alcanzado]" vertex="1">
          <mxGeometry height="16" width="1472" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-25" parent="1rj4Dn4LaAnzpcD3HqiI-23" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1526" y="96" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-26" parent="1rj4Dn4LaAnzpcD3HqiI-23" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Dentro del límite]" vertex="1">
          <mxGeometry height="16" width="1526" y="98" as="geometry" />
        </mxCell>
        <UserObject label="loop" mermaidId="n:f5" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="loop" id="1rj4Dn4LaAnzpcD3HqiI-27">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="3335" width="1616" x="35" y="1499" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-28" parent="1rj4Dn4LaAnzpcD3HqiI-27" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Para cada ejemplar prestado, con vencimiento y prórrogas independientes]" vertex="1">
          <mxGeometry height="16" width="1562" x="54" y="2" as="geometry" />
        </mxCell>
        <UserObject label="opt" mermaidId="n:f6" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="opt" id="1rj4Dn4LaAnzpcD3HqiI-29">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="361" width="1276" x="325" y="1544" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-30" parent="1rj4Dn4LaAnzpcD3HqiI-29" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[El socio consulta la opción de prorrogar (GET)]" vertex="1">
          <mxGeometry height="16" width="1222" x="54" y="2" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f7" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-31">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="214" width="364" x="335" y="1681" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-32" parent="1rj4Dn4LaAnzpcD3HqiI-31" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Sin permiso, ya devuelto o fechaFin &lt;&#xa;hoy]" vertex="1">
          <mxGeometry height="32" width="310" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-33" parent="1rj4Dn4LaAnzpcD3HqiI-31" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="364" y="112" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-34" parent="1rj4Dn4LaAnzpcD3HqiI-31" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Propietario, bibliotecario o&#xa;administrador; activo y no vencido]" vertex="1">
          <mxGeometry height="32" width="364" y="114" as="geometry" />
        </mxCell>
        <UserObject label="opt" mermaidId="n:f8" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="opt" id="1rj4Dn4LaAnzpcD3HqiI-35">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="1262" width="1346" x="295" y="1915" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-36" parent="1rj4Dn4LaAnzpcD3HqiI-35" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[El socio confirma la prórroga (POST)]" vertex="1">
          <mxGeometry height="16" width="1292" x="54" y="2" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f9" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-37">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="1115" width="1326" x="305" y="2052" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-38" parent="1rj4Dn4LaAnzpcD3HqiI-37" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Sin permiso]" vertex="1">
          <mxGeometry height="16" width="1272" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-39" parent="1rj4Dn4LaAnzpcD3HqiI-37" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1326" y="96" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-40" parent="1rj4Dn4LaAnzpcD3HqiI-37" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Tiene permiso]" vertex="1">
          <mxGeometry height="16" width="1326" y="98" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f10" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-41">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="923" width="1306" x="315" y="2234" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-42" parent="1rj4Dn4LaAnzpcD3HqiI-41" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Ya devuelto]" vertex="1">
          <mxGeometry height="16" width="1252" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-43" parent="1rj4Dn4LaAnzpcD3HqiI-41" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1306" y="96" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-44" parent="1rj4Dn4LaAnzpcD3HqiI-41" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[fechaFin &lt; hoy]" vertex="1">
          <mxGeometry height="16" width="1306" y="98" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-45" parent="1rj4Dn4LaAnzpcD3HqiI-41" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1306" y="187" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-46" parent="1rj4Dn4LaAnzpcD3HqiI-41" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Activo y no vencido]" vertex="1">
          <mxGeometry height="16" width="1306" y="189" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f11" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-47">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="594" width="1286" x="325" y="2553" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-48" parent="1rj4Dn4LaAnzpcD3HqiI-47" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Socio penalizado]" vertex="1">
          <mxGeometry height="16" width="1232" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-49" parent="1rj4Dn4LaAnzpcD3HqiI-47" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1286" y="142" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-50" parent="1rj4Dn4LaAnzpcD3HqiI-47" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Socio no penalizado]" vertex="1">
          <mxGeometry height="16" width="1286" y="144" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f12" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-51">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="356" width="1266" x="335" y="2781" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-52" parent="1rj4Dn4LaAnzpcD3HqiI-51" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[No quedan prórrogas]" vertex="1">
          <mxGeometry height="16" width="1212" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-53" parent="1rj4Dn4LaAnzpcD3HqiI-51" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1266" y="96" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-54" parent="1rj4Dn4LaAnzpcD3HqiI-51" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Quedan prórrogas]" vertex="1">
          <mxGeometry height="16" width="1266" y="98" as="geometry" />
        </mxCell>
        <UserObject label="opt" mermaidId="n:f13" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="opt" id="1rj4Dn4LaAnzpcD3HqiI-55">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="619" width="942" x="669" y="3251" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-56" parent="1rj4Dn4LaAnzpcD3HqiI-55" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Se consulta la penalización o se intenta un nuevo&#xa;préstamo]" vertex="1">
          <mxGeometry height="32" width="888" x="54" y="2" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f14" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-57">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="456" width="922" x="679" y="3404" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-58" parent="1rj4Dn4LaAnzpcD3HqiI-57" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Uno o más vencidos]" vertex="1">
          <mxGeometry height="16" width="868" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-59" parent="1rj4Dn4LaAnzpcD3HqiI-57" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="922" y="142" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-60" parent="1rj4Dn4LaAnzpcD3HqiI-57" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[No hay vencidos y castigo temporal expirado]" vertex="1">
          <mxGeometry height="16" width="922" y="144" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-61" parent="1rj4Dn4LaAnzpcD3HqiI-57" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="922" y="279" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-62" parent="1rj4Dn4LaAnzpcD3HqiI-57" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[No hay vencidos y castigo vigente]" vertex="1">
          <mxGeometry height="16" width="922" y="281" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-63" parent="1rj4Dn4LaAnzpcD3HqiI-57" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="922" y="370" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-64" parent="1rj4Dn4LaAnzpcD3HqiI-57" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[No hay vencidos ni castigo vigente]" vertex="1">
          <mxGeometry height="16" width="922" y="372" as="geometry" />
        </mxCell>
        <UserObject label="opt" mermaidId="n:f15" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="opt" id="1rj4Dn4LaAnzpcD3HqiI-65">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="944" width="1586" x="45" y="3880" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-66" parent="1rj4Dn4LaAnzpcD3HqiI-65" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Bibliotecario registra una devolución]" vertex="1">
          <mxGeometry height="16" width="1532" x="54" y="2" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f16" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-67">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="797" width="1566" x="55" y="4017" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-68" parent="1rj4Dn4LaAnzpcD3HqiI-67" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Ya devuelto]" vertex="1">
          <mxGeometry height="16" width="1512" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-69" parent="1rj4Dn4LaAnzpcD3HqiI-67" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1566" y="96" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-70" parent="1rj4Dn4LaAnzpcD3HqiI-67" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Activo]" vertex="1">
          <mxGeometry height="16" width="1566" y="98" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f17" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-71">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="559" width="1546" x="65" y="4245" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-72" parent="1rj4Dn4LaAnzpcD3HqiI-71" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Devolución en plazo (hoy &lt;= fechaFin)]" vertex="1">
          <mxGeometry height="16" width="1492" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-73" parent="1rj4Dn4LaAnzpcD3HqiI-71" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1546" y="143" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-74" parent="1rj4Dn4LaAnzpcD3HqiI-71" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Devolución tardía (hoy &gt; fechaFin)]" vertex="1">
          <mxGeometry height="16" width="1546" y="145" as="geometry" />
        </mxCell>
        <UserObject label="alt" mermaidId="n:f18" mermaidBaseStyle="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" mermaidBaseValue="alt" id="1rj4Dn4LaAnzpcD3HqiI-75">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;shape=umlFrame;dashed=1;fixDash=1;dashPattern=2 2;strokeWidth=2;pointerEvents=0;dropTarget=0;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontSize=16;align=center;verticalAlign=middle;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);height=20;width=50;" vertex="1">
            <mxGeometry height="274" width="1526" x="75" y="4520" as="geometry" />
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-76" parent="1rj4Dn4LaAnzpcD3HqiI-75" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Quedan otros vencidos (numCaducados &gt; 0)]" vertex="1">
          <mxGeometry height="16" width="1472" x="54" y="2" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-77" parent="1rj4Dn4LaAnzpcD3HqiI-75" style="shape=line;dashed=1;fixDash=1;dashPattern=2 2;strokeColor=light-dark(#9370DB,#cccccc);" vertex="1">
          <mxGeometry height="1" width="1526" y="142" as="geometry" />
        </mxCell>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-78" parent="1rj4Dn4LaAnzpcD3HqiI-75" style="text;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontSize=16;fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);" value="[Era el último vencido (numCaducados = 0)]" vertex="1">
          <mxGeometry height="16" width="1526" y="144" as="geometry" />
        </mxCell>
        <UserObject label="POST prestar_ejemplar(ejemplar, socio)" mermaidId="e:B-&gt;V#0" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="POST prestar_ejemplar(ejemplar, socio)" id="1rj4Dn4LaAnzpcD3HqiI-79">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-3" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="188" />
              </Array>
              <mxPoint x="85" y="188" as="sourcePoint" />
              <mxPoint x="689" y="188" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-80" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="1" vertex="1">
          <mxGeometry height="20" width="20" x="75" y="178" as="geometry" />
        </mxCell>
        <UserObject label="Comprobar obra prestable y ejemplar disponible" mermaidId="e:V-&gt;DB#0" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Comprobar obra prestable y ejemplar disponible" id="1rj4Dn4LaAnzpcD3HqiI-81">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1140" y="234" />
              </Array>
              <mxPoint x="689" y="234" as="sourcePoint" />
              <mxPoint x="1591" y="234" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-82" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="2" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="224" as="geometry" />
        </mxCell>
        <UserObject label="Rechazo; no se crea préstamo" mermaidId="e:V-&gt;B#0" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazo; no se crea préstamo" id="1rj4Dn4LaAnzpcD3HqiI-83">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="325" />
              </Array>
              <mxPoint x="689" y="325" as="sourcePoint" />
              <mxPoint x="85" y="325" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-84" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="3" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="315" as="geometry" />
        </mxCell>
        <UserObject label="consultar esta_penalizado" mermaidId="e:V-&gt;SM#0" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="consultar esta_penalizado" id="1rj4Dn4LaAnzpcD3HqiI-85">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-6">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="416" />
              </Array>
              <mxPoint x="689" y="416" as="sourcePoint" />
              <mxPoint x="1103" y="416" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-86" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="4" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="406" as="geometry" />
        </mxCell>
        <UserObject label="Contar préstamos con fechaDevolucion nula y fechaFin &lt; hoy" mermaidId="e:SM-&gt;DB#0" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Contar préstamos con fechaDevolucion nula y fechaFin &lt; hoy" id="1rj4Dn4LaAnzpcD3HqiI-87">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1347" y="462" />
              </Array>
              <mxPoint x="1103" y="462" as="sourcePoint" />
              <mxPoint x="1591" y="462" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-88" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="5" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="452" as="geometry" />
        </mxCell>
        <UserObject label="Guardar estado indefinido y fechaPenalizacion nula" mermaidId="e:SM-&gt;DB#1" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Guardar estado indefinido y fechaPenalizacion nula" id="1rj4Dn4LaAnzpcD3HqiI-89">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1347" y="553" />
              </Array>
              <mxPoint x="1103" y="553" as="sourcePoint" />
              <mxPoint x="1591" y="553" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-90" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="6" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="543" as="geometry" />
        </mxCell>
        <UserObject label="Penalizado" mermaidId="e:SM-&gt;V#0" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Penalizado" id="1rj4Dn4LaAnzpcD3HqiI-91">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="599" />
              </Array>
              <mxPoint x="1103" y="599" as="sourcePoint" />
              <mxPoint x="689" y="599" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-92" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="7" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="589" as="geometry" />
        </mxCell>
        <UserObject label="Rechazar préstamo" mermaidId="e:V-&gt;B#1" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazar préstamo" id="1rj4Dn4LaAnzpcD3HqiI-93">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="645" />
              </Array>
              <mxPoint x="689" y="645" as="sourcePoint" />
              <mxPoint x="85" y="645" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-94" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="8" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="635" as="geometry" />
        </mxCell>
        <UserObject label="Penalizado" mermaidId="e:SM-&gt;V#1" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Penalizado" id="1rj4Dn4LaAnzpcD3HqiI-95">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="781" />
              </Array>
              <mxPoint x="1103" y="781" as="sourcePoint" />
              <mxPoint x="689" y="781" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-96" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="9" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="771" as="geometry" />
        </mxCell>
        <UserObject label="Rechazar préstamo" mermaidId="e:V-&gt;B#2" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazar préstamo" id="1rj4Dn4LaAnzpcD3HqiI-97">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="827" />
              </Array>
              <mxPoint x="689" y="827" as="sourcePoint" />
              <mxPoint x="85" y="827" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-98" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="10" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="817" as="geometry" />
        </mxCell>
        <UserObject label="Limpiar estado temporal" mermaidId="e:SM-&gt;DB#2" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Limpiar estado temporal" id="1rj4Dn4LaAnzpcD3HqiI-99">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1347" y="918" />
              </Array>
              <mxPoint x="1103" y="918" as="sourcePoint" />
              <mxPoint x="1591" y="918" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-100" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="11" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="908" as="geometry" />
        </mxCell>
        <UserObject label="No penalizado" mermaidId="e:SM-&gt;V#2" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="No penalizado" id="1rj4Dn4LaAnzpcD3HqiI-101">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="964" />
              </Array>
              <mxPoint x="1103" y="964" as="sourcePoint" />
              <mxPoint x="689" y="964" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-102" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="12" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="954" as="geometry" />
        </mxCell>
        <UserObject label="No penalizado" mermaidId="e:SM-&gt;V#3" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="No penalizado" id="1rj4Dn4LaAnzpcD3HqiI-103">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="1055" />
              </Array>
              <mxPoint x="1103" y="1055" as="sourcePoint" />
              <mxPoint x="689" y="1055" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-104" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="13" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="1045" as="geometry" />
        </mxCell>
        <UserObject label="Contar préstamos activos del tipo de obra" mermaidId="e:V-&gt;DB#1" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Contar préstamos activos del tipo de obra" id="1rj4Dn4LaAnzpcD3HqiI-105">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1140" y="1111" />
              </Array>
              <mxPoint x="689" y="1111" as="sourcePoint" />
              <mxPoint x="1591" y="1111" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-106" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="14" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="1101" as="geometry" />
        </mxCell>
        <UserObject label="Rechazar préstamo" mermaidId="e:V-&gt;B#3" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazar préstamo" id="1rj4Dn4LaAnzpcD3HqiI-107">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="1202" />
              </Array>
              <mxPoint x="689" y="1202" as="sourcePoint" />
              <mxPoint x="85" y="1202" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-108" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="15" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="1192" as="geometry" />
        </mxCell>
        <UserObject label="Crear préstamo del ejemplar" mermaidId="e:V-&gt;PM#0" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Crear préstamo del ejemplar" id="1rj4Dn4LaAnzpcD3HqiI-109">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-7">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1018" y="1293" />
              </Array>
              <mxPoint x="689" y="1293" as="sourcePoint" />
              <mxPoint x="1347" y="1293" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-110" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="16" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="1283" as="geometry" />
        </mxCell>
        <UserObject label="Guardar préstamo activo" mermaidId="e:PM-&gt;DB#0" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Guardar préstamo activo" id="1rj4Dn4LaAnzpcD3HqiI-111">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-7" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1469" y="1403" />
              </Array>
              <mxPoint x="1347" y="1403" as="sourcePoint" />
              <mxPoint x="1591" y="1403" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-112" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="17" vertex="1">
          <mxGeometry height="20" width="20" x="1337" y="1393" as="geometry" />
        </mxCell>
        <UserObject label="Préstamo registrado" mermaidId="e:V-&gt;B#4" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Préstamo registrado" id="1rj4Dn4LaAnzpcD3HqiI-113">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="1449" />
              </Array>
              <mxPoint x="689" y="1449" as="sourcePoint" />
              <mxPoint x="85" y="1449" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-114" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="18" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="1439" as="geometry" />
        </mxCell>
        <UserObject label="GET prorrogar_prestamo(id)" mermaidId="e:S-&gt;V#0" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="GET prorrogar_prestamo(id)" id="1rj4Dn4LaAnzpcD3HqiI-115">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-4" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="1625" />
              </Array>
              <mxPoint x="345" y="1625" as="sourcePoint" />
              <mxPoint x="689" y="1625" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-116" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="19" vertex="1">
          <mxGeometry height="20" width="20" x="335" y="1615" as="geometry" />
        </mxCell>
        <UserObject label="Obtener préstamo, socio y propietario" mermaidId="e:V-&gt;DB#2" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Obtener préstamo, socio y propietario" id="1rj4Dn4LaAnzpcD3HqiI-117">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1140" y="1671" />
              </Array>
              <mxPoint x="689" y="1671" as="sourcePoint" />
              <mxPoint x="1591" y="1671" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-118" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="20" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="1661" as="geometry" />
        </mxCell>
        <UserObject label="Rechazo; no modificar préstamo" mermaidId="e:V-&gt;S#0" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazo; no modificar préstamo" id="1rj4Dn4LaAnzpcD3HqiI-119">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="1778" />
              </Array>
              <mxPoint x="689" y="1778" as="sourcePoint" />
              <mxPoint x="345" y="1778" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-120" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="21" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="1768" as="geometry" />
        </mxCell>
        <UserObject label="Mostrar confirmación y días configurados" mermaidId="e:V-&gt;S#1" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Mostrar confirmación y días configurados" id="1rj4Dn4LaAnzpcD3HqiI-121">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="1885" />
              </Array>
              <mxPoint x="689" y="1885" as="sourcePoint" />
              <mxPoint x="345" y="1885" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-122" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="22" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="1875" as="geometry" />
        </mxCell>
        <UserObject label="POST prorrogar_prestamo(id)" mermaidId="e:S-&gt;V#1" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="POST prorrogar_prestamo(id)" id="1rj4Dn4LaAnzpcD3HqiI-123">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-4" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="1996" />
              </Array>
              <mxPoint x="345" y="1996" as="sourcePoint" />
              <mxPoint x="689" y="1996" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-124" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="23" vertex="1">
          <mxGeometry height="20" width="20" x="335" y="1986" as="geometry" />
        </mxCell>
        <UserObject label="Obtener préstamo y comprobar permiso" mermaidId="e:V-&gt;DB#3" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Obtener préstamo y comprobar permiso" id="1rj4Dn4LaAnzpcD3HqiI-125">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1140" y="2042" />
              </Array>
              <mxPoint x="689" y="2042" as="sourcePoint" />
              <mxPoint x="1591" y="2042" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-126" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="24" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2032" as="geometry" />
        </mxCell>
        <UserObject label="Rechazar" mermaidId="e:V-&gt;S#2" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazar" id="1rj4Dn4LaAnzpcD3HqiI-127">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="2133" />
              </Array>
              <mxPoint x="689" y="2133" as="sourcePoint" />
              <mxPoint x="345" y="2133" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-128" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="25" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2123" as="geometry" />
        </mxCell>
        <UserObject label="Comprobar fechaDevolucion y fechaFin" mermaidId="e:V-&gt;PM#1" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Comprobar fechaDevolucion y fechaFin" id="1rj4Dn4LaAnzpcD3HqiI-129">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-7">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1018" y="2224" />
              </Array>
              <mxPoint x="689" y="2224" as="sourcePoint" />
              <mxPoint x="1347" y="2224" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-130" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="26" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2214" as="geometry" />
        </mxCell>
        <UserObject label="Rechazar; préstamo ya devuelto" mermaidId="e:V-&gt;S#3" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazar; préstamo ya devuelto" id="1rj4Dn4LaAnzpcD3HqiI-131">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="2315" />
              </Array>
              <mxPoint x="689" y="2315" as="sourcePoint" />
              <mxPoint x="345" y="2315" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-132" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="27" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2305" as="geometry" />
        </mxCell>
        <UserObject label="Rechazar; debe devolver el vencido" mermaidId="e:V-&gt;S#4" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazar; debe devolver el vencido" id="1rj4Dn4LaAnzpcD3HqiI-133">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="2406" />
              </Array>
              <mxPoint x="689" y="2406" as="sourcePoint" />
              <mxPoint x="345" y="2406" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-134" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="28" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2396" as="geometry" />
        </mxCell>
        <UserObject label="consultar esta_penalizado" mermaidId="e:V-&gt;SM#1" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="consultar esta_penalizado" id="1rj4Dn4LaAnzpcD3HqiI-135">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-6">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="2497" />
              </Array>
              <mxPoint x="689" y="2497" as="sourcePoint" />
              <mxPoint x="1103" y="2497" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-136" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="29" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2487" as="geometry" />
        </mxCell>
        <UserObject label="Recalcular vencidos activos del socio" mermaidId="e:SM-&gt;DB#3" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Recalcular vencidos activos del socio" id="1rj4Dn4LaAnzpcD3HqiI-137">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1347" y="2543" />
              </Array>
              <mxPoint x="1103" y="2543" as="sourcePoint" />
              <mxPoint x="1591" y="2543" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-138" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="30" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="2533" as="geometry" />
        </mxCell>
        <UserObject label="Penalizado" mermaidId="e:SM-&gt;V#4" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Penalizado" id="1rj4Dn4LaAnzpcD3HqiI-139">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="2634" />
              </Array>
              <mxPoint x="1103" y="2634" as="sourcePoint" />
              <mxPoint x="689" y="2634" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-140" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="31" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="2624" as="geometry" />
        </mxCell>
        <UserObject label="Rechazar prórroga" mermaidId="e:V-&gt;S#5" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazar prórroga" id="1rj4Dn4LaAnzpcD3HqiI-141">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="2680" />
              </Array>
              <mxPoint x="689" y="2680" as="sourcePoint" />
              <mxPoint x="345" y="2680" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-142" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="32" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2670" as="geometry" />
        </mxCell>
        <UserObject label="Comprobar prorrogasRestantes" mermaidId="e:V-&gt;PM#2" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Comprobar prorrogasRestantes" id="1rj4Dn4LaAnzpcD3HqiI-143">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-7">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1018" y="2771" />
              </Array>
              <mxPoint x="689" y="2771" as="sourcePoint" />
              <mxPoint x="1347" y="2771" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-144" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="33" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2761" as="geometry" />
        </mxCell>
        <UserObject label="Rechazar; no quedan prórrogas" mermaidId="e:V-&gt;S#6" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Rechazar; no quedan prórrogas" id="1rj4Dn4LaAnzpcD3HqiI-145">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="2862" />
              </Array>
              <mxPoint x="689" y="2862" as="sourcePoint" />
              <mxPoint x="345" y="2862" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-146" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="34" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2852" as="geometry" />
        </mxCell>
        <UserObject label="Aplicar prórroga" mermaidId="e:V-&gt;PM#3" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Aplicar prórroga" id="1rj4Dn4LaAnzpcD3HqiI-147">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-7">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1018" y="2953" />
              </Array>
              <mxPoint x="689" y="2953" as="sourcePoint" />
              <mxPoint x="1347" y="2953" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-148" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="35" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="2943" as="geometry" />
        </mxCell>
        <UserObject label="Guardar fechas y contador" mermaidId="e:PM-&gt;DB#1" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Guardar fechas y contador" id="1rj4Dn4LaAnzpcD3HqiI-149">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-7" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1469" y="3081" />
              </Array>
              <mxPoint x="1347" y="3081" as="sourcePoint" />
              <mxPoint x="1591" y="3081" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-150" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="36" vertex="1">
          <mxGeometry height="20" width="20" x="1337" y="3071" as="geometry" />
        </mxCell>
        <UserObject label="Confirmar nueva fecha de devolución" mermaidId="e:V-&gt;S#7" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Confirmar nueva fecha de devolución" id="1rj4Dn4LaAnzpcD3HqiI-151">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="517" y="3127" />
              </Array>
              <mxPoint x="689" y="3127" as="sourcePoint" />
              <mxPoint x="345" y="3127" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-152" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="37" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="3117" as="geometry" />
        </mxCell>
        <UserObject label="consultar esta_penalizado" mermaidId="e:V-&gt;SM#2" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="consultar esta_penalizado" id="1rj4Dn4LaAnzpcD3HqiI-153">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-6">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="3348" />
              </Array>
              <mxPoint x="689" y="3348" as="sourcePoint" />
              <mxPoint x="1103" y="3348" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-154" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="38" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="3338" as="geometry" />
        </mxCell>
        <UserObject label="Contar todos los préstamos vencidos sin devolver" mermaidId="e:SM-&gt;DB#4" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Contar todos los préstamos vencidos sin devolver" id="1rj4Dn4LaAnzpcD3HqiI-155">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1347" y="3394" />
              </Array>
              <mxPoint x="1103" y="3394" as="sourcePoint" />
              <mxPoint x="1591" y="3394" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-156" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="39" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="3384" as="geometry" />
        </mxCell>
        <UserObject label="Guardar estado indefinido" mermaidId="e:SM-&gt;DB#5" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Guardar estado indefinido" id="1rj4Dn4LaAnzpcD3HqiI-157">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1347" y="3485" />
              </Array>
              <mxPoint x="1103" y="3485" as="sourcePoint" />
              <mxPoint x="1591" y="3485" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-158" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="40" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="3475" as="geometry" />
        </mxCell>
        <UserObject label="Penalizado; numCaducados = cantidad de vencidos" mermaidId="e:SM-&gt;V#5" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Penalizado; numCaducados = cantidad de vencidos" id="1rj4Dn4LaAnzpcD3HqiI-159">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="3531" />
              </Array>
              <mxPoint x="1103" y="3531" as="sourcePoint" />
              <mxPoint x="689" y="3531" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-160" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="41" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="3521" as="geometry" />
        </mxCell>
        <UserObject label="Limpiar castigo temporal" mermaidId="e:SM-&gt;DB#6" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Limpiar castigo temporal" id="1rj4Dn4LaAnzpcD3HqiI-161">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1347" y="3622" />
              </Array>
              <mxPoint x="1103" y="3622" as="sourcePoint" />
              <mxPoint x="1591" y="3622" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-162" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="42" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="3612" as="geometry" />
        </mxCell>
        <UserObject label="No penalizado" mermaidId="e:SM-&gt;V#6" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="No penalizado" id="1rj4Dn4LaAnzpcD3HqiI-163">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="3668" />
              </Array>
              <mxPoint x="1103" y="3668" as="sourcePoint" />
              <mxPoint x="689" y="3668" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-164" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="43" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="3658" as="geometry" />
        </mxCell>
        <UserObject label="Penalizado temporalmente" mermaidId="e:SM-&gt;V#7" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Penalizado temporalmente" id="1rj4Dn4LaAnzpcD3HqiI-165">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="3759" />
              </Array>
              <mxPoint x="1103" y="3759" as="sourcePoint" />
              <mxPoint x="689" y="3759" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-166" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="44" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="3749" as="geometry" />
        </mxCell>
        <UserObject label="Sin castigo" mermaidId="e:SM-&gt;V#8" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Sin castigo" id="1rj4Dn4LaAnzpcD3HqiI-167">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="3850" />
              </Array>
              <mxPoint x="1103" y="3850" as="sourcePoint" />
              <mxPoint x="689" y="3850" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-168" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="45" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="3840" as="geometry" />
        </mxCell>
        <UserObject label="POST devolver_ejemplar(id)" mermaidId="e:B-&gt;V#1" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="POST devolver_ejemplar(id)" id="1rj4Dn4LaAnzpcD3HqiI-169">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-3" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="3961" />
              </Array>
              <mxPoint x="85" y="3961" as="sourcePoint" />
              <mxPoint x="689" y="3961" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-170" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="46" vertex="1">
          <mxGeometry height="20" width="20" x="75" y="3951" as="geometry" />
        </mxCell>
        <UserObject label="Comprobar que sigue activo" mermaidId="e:V-&gt;PM#4" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Comprobar que sigue activo" id="1rj4Dn4LaAnzpcD3HqiI-171">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-7">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1018" y="4007" />
              </Array>
              <mxPoint x="689" y="4007" as="sourcePoint" />
              <mxPoint x="1347" y="4007" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-172" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="47" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="3997" as="geometry" />
        </mxCell>
        <UserObject label="Informar; sin cambios" mermaidId="e:V-&gt;B#5" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Informar; sin cambios" id="1rj4Dn4LaAnzpcD3HqiI-173">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="4098" />
              </Array>
              <mxPoint x="689" y="4098" as="sourcePoint" />
              <mxPoint x="85" y="4098" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-174" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="48" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="4088" as="geometry" />
        </mxCell>
        <UserObject label="Guardar fechaDevolucion = hoy" mermaidId="e:V-&gt;DB#4" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Guardar fechaDevolucion = hoy" id="1rj4Dn4LaAnzpcD3HqiI-175">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1140" y="4189" />
              </Array>
              <mxPoint x="689" y="4189" as="sourcePoint" />
              <mxPoint x="1591" y="4189" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-176" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="49" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="4179" as="geometry" />
        </mxCell>
        <UserObject label="Comparar hoy con fechaFin" mermaidId="e:V-&gt;PM#5" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Comparar hoy con fechaFin" id="1rj4Dn4LaAnzpcD3HqiI-177">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-7">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1018" y="4235" />
              </Array>
              <mxPoint x="689" y="4235" as="sourcePoint" />
              <mxPoint x="1347" y="4235" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-178" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="50" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="4225" as="geometry" />
        </mxCell>
        <UserObject label="Devolución registrada" mermaidId="e:V-&gt;B#6" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Devolución registrada" id="1rj4Dn4LaAnzpcD3HqiI-179">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="4373" />
              </Array>
              <mxPoint x="689" y="4373" as="sourcePoint" />
              <mxPoint x="85" y="4373" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-180" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="51" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="4363" as="geometry" />
        </mxCell>
        <UserObject label="Consultar numCaducados tras guardar devolución" mermaidId="e:V-&gt;SM#3" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Consultar numCaducados tras guardar devolución" id="1rj4Dn4LaAnzpcD3HqiI-181">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-6">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="896" y="4464" />
              </Array>
              <mxPoint x="689" y="4464" as="sourcePoint" />
              <mxPoint x="1103" y="4464" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-182" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="52" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="4454" as="geometry" />
        </mxCell>
        <UserObject label="Contar otros préstamos vencidos aún sin devolver" mermaidId="e:SM-&gt;DB#7" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Contar otros préstamos vencidos aún sin devolver" id="1rj4Dn4LaAnzpcD3HqiI-183">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-6" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1347" y="4510" />
              </Array>
              <mxPoint x="1103" y="4510" as="sourcePoint" />
              <mxPoint x="1591" y="4510" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-184" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="53" vertex="1">
          <mxGeometry height="20" width="20" x="1093" y="4500" as="geometry" />
        </mxCell>
        <UserObject label="Mantener/guardar penalización indefinida" mermaidId="e:V-&gt;DB#5" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Mantener/guardar penalización indefinida" id="1rj4Dn4LaAnzpcD3HqiI-185">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1140" y="4601" />
              </Array>
              <mxPoint x="689" y="4601" as="sourcePoint" />
              <mxPoint x="1591" y="4601" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-186" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="54" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="4591" as="geometry" />
        </mxCell>
        <UserObject label="Devolución registrada; persiste la penalización indefinida" mermaidId="e:V-&gt;B#7" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Devolución registrada; persiste la penalización indefinida" id="1rj4Dn4LaAnzpcD3HqiI-187">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="4647" />
              </Array>
              <mxPoint x="689" y="4647" as="sourcePoint" />
              <mxPoint x="85" y="4647" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-188" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="55" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="4637" as="geometry" />
        </mxCell>
        <UserObject label="Guardar castigo temporal con fechaPenalizacion = hoy" mermaidId="e:V-&gt;DB#6" mermaidBaseStyle="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Guardar castigo temporal con fechaPenalizacion = hoy" id="1rj4Dn4LaAnzpcD3HqiI-189">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1140" y="4738" />
              </Array>
              <mxPoint x="689" y="4738" as="sourcePoint" />
              <mxPoint x="1591" y="4738" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-190" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="56" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="4728" as="geometry" />
        </mxCell>
        <UserObject label="Devolución registrada; comienza o se reinicia el castigo temporal" mermaidId="e:V-&gt;B#8" mermaidBaseStyle="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" mermaidBaseValue="Devolución registrada; comienza o se reinicia el castigo temporal" id="1rj4Dn4LaAnzpcD3HqiI-191">
          <mxCell edge="1" parent="PjRlD1XJtcLBet5u5arM-0" source="1rj4Dn4LaAnzpcD3HqiI-5" style="dashed=1;fixDash=1;dashPattern=3 3;endArrow=block;endSize=9;verticalAlign=bottom;spacingBottom=2;edgeStyle=sequenceEdgeStyle;libavoidRouting=0;curved=0;rounded=0;fontSize=16;labelBackgroundColor=none;strokeWidth=1.5;strokeColor=light-dark(#333333,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;" target="1rj4Dn4LaAnzpcD3HqiI-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="387" y="4784" />
              </Array>
              <mxPoint x="689" y="4784" as="sourcePoint" />
              <mxPoint x="85" y="4784" as="targetPoint" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <mxCell id="1rj4Dn4LaAnzpcD3HqiI-192" parent="PjRlD1XJtcLBet5u5arM-0" style="ellipse;aspect=fixed;fillColor=light-dark(#333333,#cccccc);align=center;verticalAlign=middle;fontColor=light-dark(#FFFFFF,#333333);fontSize=12;" value="57" vertex="1">
          <mxGeometry height="20" width="20" x="679" y="4774" as="geometry" />
        </mxCell>
        <UserObject label="Alta de préstamo (una solicitud por ejemplar)" mermaidId="n:note0" mermaidBaseStyle="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Alta de préstamo (una solicitud por ejemplar)" id="1rj4Dn4LaAnzpcD3HqiI-193">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="37" width="1556" x="60" y="105" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="fechaFin = hoy + DIAS_PRESTAMO&#xa;prorrogasRestantes = PRORROGAS_INICIALES" mermaidId="n:note1" mermaidBaseStyle="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="fechaFin = hoy + DIAS_PRESTAMO&#xa;prorrogasRestantes = PRORROGAS_INICIALES" id="1rj4Dn4LaAnzpcD3HqiI-194">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="316" x="1189" y="1303" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="fechaFin += DIAS_PRORROGA&#xa;fechaProrroga = hoy&#xa;prorrogasRestantes -= 1" mermaidId="n:note2" mermaidBaseStyle="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="fechaFin += DIAS_PRORROGA&#xa;fechaProrroga = hoy&#xa;prorrogasRestantes -= 1" id="1rj4Dn4LaAnzpcD3HqiI-195">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="72" width="206" x="1244" y="2963" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Al pasar la fecha fin, el préstamo solo cuenta como vencido si no se ha devuelto.&#xa;La comprobación es fechaFin &lt; hoy; no hay transición automática por un proceso en segundo plano." mermaidId="n:note3" mermaidBaseStyle="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Al pasar la fecha fin, el préstamo solo cuenta como vencido si no se ha devuelto.&#xa;La comprobación es fechaFin &lt; hoy; no hay transición automática por un proceso en segundo plano." id="1rj4Dn4LaAnzpcD3HqiI-196">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="1296" x="320" y="3187" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="No cambia el estado de penalización" mermaidId="n:note4" mermaidBaseStyle="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="No cambia el estado de penalización" id="1rj4Dn4LaAnzpcD3HqiI-197">
          <mxCell parent="PjRlD1XJtcLBet5u5arM-0" style="html=1;fillColor=light-dark(#fff5ad,#2a2a2a);strokeColor=light-dark(#aaaa33,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="37" width="464" x="664" y="4290" as="geometry" />
          </mxCell>
        </UserObject>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>

```

## Relación con los tests

El flujo contempla los escenarios de [tests.py](./liber/backend/liber/prestamos/tests.py): socio nuevo y sin penalización, préstamo vencido, vencimiento durante castigo temporal, expiración del castigo, alta permitida/rechazada, confirmación de prórroga con duración configurada, devolución en plazo, devolución de uno o del último de varios vencidos y reinicio del castigo al devolver tarde.
