# Diagrama de flujo: préstamos, caducidad y prórrogas

```drawio
<mxfile>
  <diagram id="fy0EKL-jXhviKVUWZTJA" name="Page-1">
    <mxGraphModel dx="6400" dy="6544" grid="1" gridSize="10" guides="1" tooltips="0" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="8F7osiW-PJWJIescSTIe-0" />
        <mxCell id="8F7osiW-PJWJIescSTIe-1" parent="8F7osiW-PJWJIescSTIe-0" />
        <UserObject label="" mermaidData="{&#xa;  &quot;data&quot;: &quot;flowchart TD\r\n    A([Inicio: bibliotecario intenta prestar un ejemplar]) --&gt; B{¿Obra prestable y ejemplar disponible?}\r\n    B -- No --&gt; B1[No se crea el préstamo]\r\n    B -- Sí --&gt; C{¿Socio válido?}\r\n    C -- No --&gt; C1[Mostrar error: socio no seleccionado o inexistente]\r\n    C -- Sí --&gt; D[Calcular préstamos vencidos sin devolver del socio]\r\n    D --&gt; E{¿Hay algún préstamo vencido?}\r\n    E -- Sí --&gt; E1[Marcar penalización indefinida&lt;br/&gt;fecha de penalización vacía]\r\n    E1 --&gt; X[Rechazar nuevo préstamo]\r\n    E -- No --&gt; F{¿Tiene castigo temporal vigente?}\r\n    F -- Sí --&gt; X\r\n    F -- No; ya venció el castigo --&gt; F1[Limpiar castigo temporal]\r\n    F -- No; sin castigo --&gt; G[Comprobar límite de préstamos activos&lt;br/&gt;por tipo de obra]\r\n    F1 --&gt; G\r\n    G --&gt; H{¿Alcanza el límite?}\r\n    H -- Sí --&gt; H1[Rechazar nuevo préstamo]\r\n    H -- No --&gt; I[Crear préstamo para este ejemplar&lt;br/&gt;fechaFin = hoy + días de préstamo&lt;br/&gt;prórrogas disponibles = iniciales]\r\n    I --&gt; J[El préstamo queda activo&lt;br/&gt;Cada ejemplar tiene fechas y prórrogas propias]\r\n\r\n    J --&gt; K{¿El socio solicita prórroga?}\r\n    K -- No --&gt; L{¿Se registra una devolución?}\r\n    L -- Sí --&gt; AA{¿hoy &gt; fechaFin?}\r\n    AA -- No --&gt; AB[Registrar devolución en plazo&lt;br/&gt;no altera castigo temporal existente]\r\n    AB --&gt; AC([Fin de este préstamo])\r\n    AA -- Sí --&gt; W[Marcar fechaDevolucion = hoy&lt;br/&gt;recalcular otros vencidos activos]\r\n    L -- No --&gt; AD{¿fechaFin es anterior a hoy?}\r\n    AD -- No --&gt; J\r\n    AD -- Sí --&gt; S[El préstamo sigue activo y cuenta como vencido]\r\n    S --&gt; T[Al consultar la penalización o intentar otro préstamo,&lt;br/&gt;recalcular vencidos activos]\r\n    T --&gt; U{¿Hay uno o más vencidos?}\r\n    U -- Sí --&gt; U1[Penalización indefinida&lt;br/&gt;no puede recibir préstamos ni prorrogar]\r\n    U1 --&gt; V{¿Se devuelve un ejemplar vencido?}\r\n    V -- No --&gt; S\r\n    V -- Sí --&gt; W\r\n\r\n    K -- Sí --&gt; M{¿Tiene permiso y el préstamo sigue activo?}\r\n    M -- No --&gt; M1[Rechazar: sin permiso o ya devuelto]\r\n    M -- Sí --&gt; N{¿fechaFin es anterior a hoy?}\r\n    N -- Sí --&gt; N1[Rechazar prórroga: vencido&lt;br/&gt;debe devolverse primero]\r\n    N -- No --&gt; O{¿Es una consulta GET?}\r\n    O -- Sí --&gt; O1[Mostrar confirmación&lt;br/&gt;sin modificar préstamo]\r\n    O -- No --&gt; P{¿Socio penalizado?}\r\n    P -- Sí --&gt; P1[Rechazar prórroga]\r\n    P -- No --&gt; Q{¿Quedan prórrogas para este ejemplar?}\r\n    Q -- No --&gt; Q1[Rechazar: no quedan prórrogas]\r\n    Q -- Sí --&gt; R[Sumar días de prórroga a fechaFin&lt;br/&gt;guardar fechaProrroga y descontar 1]\r\n    R --&gt; J\r\n\r\n    W --&gt; Y{¿Queda algún otro vencido sin devolver?}\r\n    Y -- Sí --&gt; Y1[Mantener penalización indefinida&lt;br/&gt;numCaducados refleja los restantes]\r\n    Y1 --&gt; V\r\n    Y -- No --&gt; Z[Iniciar o reiniciar castigo temporal&lt;br/&gt;fechaPenalizacion = hoy]\r\n    Z --&gt; Z1{¿Termina el plazo del castigo&lt;br/&gt;y no hay nuevos vencidos?}\r\n    Z1 -- No --&gt; Z2[Sigue penalizado durante el plazo]\r\n    Z2 --&gt; Z1\r\n    Z1 -- Sí --&gt; Z3[Limpiar castigo&lt;br/&gt;estado sin castigo]\r\n    Z3 --&gt; G&quot;,&#xa;  &quot;config&quot;: null&#xa;}" id="85LOYg6x6uEBZxuNiowh-0">
          <mxCell connectable="0" parent="8F7osiW-PJWJIescSTIe-1" style="group;transparentBounds=1;editIcon=1;lockedGroup=0;groupPadding=10;" vertex="1">
            <mxGeometry as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Inicio: bibliotecario intenta prestar un ejemplar" mermaidId="n:A" mermaidBaseStyle="html=1;rounded=1;whiteSpace=wrap;arcSize=50;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Inicio: bibliotecario intenta prestar un ejemplar" id="8F7osiW-PJWJIescSTIe-2">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;rounded=1;whiteSpace=wrap;arcSize=50;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="39" width="369" x="1080" y="10" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Obra prestable y ejemplar disponible?" mermaidId="n:B" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Obra prestable y ejemplar disponible?" id="8F7osiW-PJWJIescSTIe-3">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="462" width="462" x="1033" y="99" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="No se crea el préstamo" mermaidId="n:B1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="No se crea el préstamo" id="8F7osiW-PJWJIescSTIe-4">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="225" x="1028" y="689" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Socio válido?" mermaidId="n:C" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Socio válido?" id="8F7osiW-PJWJIescSTIe-5">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="171" width="171" x="1303" y="630" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Mostrar error: socio no seleccionado o inexistente" mermaidId="n:C1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Mostrar error: socio no seleccionado o inexistente" id="8F7osiW-PJWJIescSTIe-6">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="419" x="943" y="871" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Calcular préstamos vencidos sin devolver del socio" mermaidId="n:D" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Calcular préstamos vencidos sin devolver del socio" id="8F7osiW-PJWJIescSTIe-7">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="423" x="1412" y="871" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Hay algún préstamo vencido?" mermaidId="n:E" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Hay algún préstamo vencido?" id="8F7osiW-PJWJIescSTIe-8">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="358" width="358" x="1444" y="975" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Marcar penalización indefinida&#xa;fecha de penalización vacía" mermaidId="n:E1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Marcar penalización indefinida&#xa;fecha de penalización vacía" id="8F7osiW-PJWJIescSTIe-9">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="280" x="1291" y="1561" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Rechazar nuevo préstamo" mermaidId="n:X" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Rechazar nuevo préstamo" id="8F7osiW-PJWJIescSTIe-10">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="244" x="1322" y="1861" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Tiene castigo temporal vigente?" mermaidId="n:F" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Tiene castigo temporal vigente?" id="8F7osiW-PJWJIescSTIe-11">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="390" width="390" x="1621" y="1402" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Limpiar castigo temporal" mermaidId="n:F1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Limpiar castigo temporal" id="8F7osiW-PJWJIescSTIe-12">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="239" x="1752" y="1861" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Comprobar límite de préstamos activos&#xa;por tipo de obra" mermaidId="n:G" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Comprobar límite de préstamos activos&#xa;por tipo de obra" id="8F7osiW-PJWJIescSTIe-13">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="341" x="1804" y="1965" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Alcanza el límite?" mermaidId="n:H" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Alcanza el límite?" id="8F7osiW-PJWJIescSTIe-14">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="227" width="227" x="1376" y="2088" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Rechazar nuevo préstamo" mermaidId="n:H1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Rechazar nuevo préstamo" id="8F7osiW-PJWJIescSTIe-15">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="244" x="1204" y="2404" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Crear préstamo para este ejemplar&#xa;fechaFin = hoy + días de préstamo&#xa;prórrogas disponibles = iniciales" mermaidId="n:I" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Crear préstamo para este ejemplar&#xa;fechaFin = hoy + días de préstamo&#xa;prórrogas disponibles = iniciales" id="8F7osiW-PJWJIescSTIe-16">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="93" width="312" x="1865" y="2385" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="El préstamo queda activo&#xa;Cada ejemplar tiene fechas y prórrogas propias" mermaidId="n:J" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="El préstamo queda activo&#xa;Cada ejemplar tiene fechas y prórrogas propias" id="8F7osiW-PJWJIescSTIe-17">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="400" x="1821" y="2528" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿El socio solicita prórroga?" mermaidId="n:K" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿El socio solicita prórroga?" id="8F7osiW-PJWJIescSTIe-18">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="317" width="317" x="1352" y="2651" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Se registra una devolución?" mermaidId="n:L" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Se registra una devolución?" id="8F7osiW-PJWJIescSTIe-19">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="338" width="338" x="1010" y="3120" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿hoy &gt; fechaFin?" mermaidId="n:AA" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿hoy &gt; fechaFin?" id="8F7osiW-PJWJIescSTIe-20">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="202" width="202" x="716" y="3676" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Registrar devolución en plazo&#xa;no altera castigo temporal existente" mermaidId="n:AB" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Registrar devolución en plazo&#xa;no altera castigo temporal existente" id="8F7osiW-PJWJIescSTIe-21">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="322" x="10" y="4109" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Fin de este préstamo" mermaidId="n:AC" mermaidBaseStyle="html=1;rounded=1;whiteSpace=wrap;arcSize=50;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Fin de este préstamo" id="8F7osiW-PJWJIescSTIe-22">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;rounded=1;whiteSpace=wrap;arcSize=50;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="39" width="175" x="84" y="4565" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Marcar fechaDevolucion = hoy&#xa;recalcular otros vencidos activos" mermaidId="n:W" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Marcar fechaDevolucion = hoy&#xa;recalcular otros vencidos activos" id="8F7osiW-PJWJIescSTIe-23">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="295" x="670" y="4109" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿fechaFin es anterior a hoy?" mermaidId="n:AD" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿fechaFin es anterior a hoy?" id="8F7osiW-PJWJIescSTIe-24">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="334" width="334" x="1505" y="3609" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="El préstamo sigue activo y cuenta como vencido" mermaidId="n:S" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="El préstamo sigue activo y cuenta como vencido" id="8F7osiW-PJWJIescSTIe-25">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="405" x="1010" y="5916" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Al consultar la penalización o intentar otro préstamo,&#xa;recalcular vencidos activos" mermaidId="n:T" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Al consultar la penalización o intentar otro préstamo,&#xa;recalcular vencidos activos" id="8F7osiW-PJWJIescSTIe-26">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="446" x="990" y="6029" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Hay uno o más vencidos?" mermaidId="n:U" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Hay uno o más vencidos?" id="8F7osiW-PJWJIescSTIe-27">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="307" width="307" x="1059" y="6152" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Penalización indefinida&#xa;no puede recibir préstamos ni prorrogar" mermaidId="n:U1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Penalización indefinida&#xa;no puede recibir préstamos ni prorrogar" id="8F7osiW-PJWJIescSTIe-28">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="347" x="910" y="6529" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Se devuelve un ejemplar vencido?" mermaidId="n:V" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Se devuelve un ejemplar vencido?" id="8F7osiW-PJWJIescSTIe-29">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="414" width="414" x="465" y="5423" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Tiene permiso y el préstamo sigue activo?" mermaidId="n:M" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Tiene permiso y el préstamo sigue activo?" id="8F7osiW-PJWJIescSTIe-30">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="504" width="504" x="1804" y="3036" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Rechazar: sin permiso o ya devuelto" mermaidId="n:M1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Rechazar: sin permiso o ya devuelto" id="8F7osiW-PJWJIescSTIe-31">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="319" x="1092" y="3750" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿fechaFin es anterior a hoy?" mermaidId="n:N" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿fechaFin es anterior a hoy?" id="8F7osiW-PJWJIescSTIe-32">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="334" width="334" x="1951" y="3609" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Rechazar prórroga: vencido&#xa;debe devolverse primero" mermaidId="n:N1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Rechazar prórroga: vencido&#xa;debe devolverse primero" id="8F7osiW-PJWJIescSTIe-33">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="257" x="1818" y="4109" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Es una consulta GET?" mermaidId="n:O" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Es una consulta GET?" id="8F7osiW-PJWJIescSTIe-34">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="266" width="266" x="2142" y="4013" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Mostrar confirmación&#xa;sin modificar préstamo" mermaidId="n:O1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Mostrar confirmación&#xa;sin modificar préstamo" id="8F7osiW-PJWJIescSTIe-35">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="225" x="1982" y="4548" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Socio penalizado?" mermaidId="n:P" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Socio penalizado?" id="8F7osiW-PJWJIescSTIe-36">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="227" width="227" x="2299" y="4471" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Rechazar prórroga" mermaidId="n:P1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Rechazar prórroga" id="8F7osiW-PJWJIescSTIe-37">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="191" x="2128" y="5095" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Quedan prórrogas para este ejemplar?" mermaidId="n:Q" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Quedan prórrogas para este ejemplar?" id="8F7osiW-PJWJIescSTIe-38">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="464" width="464" x="2369" y="4890" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Rechazar: no quedan prórrogas" mermaidId="n:Q1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Rechazar: no quedan prórrogas" id="8F7osiW-PJWJIescSTIe-39">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="282" x="2294" y="5603" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Sumar días de prórroga a fechaFin&#xa;guardar fechaProrroga y descontar 1" mermaidId="n:R" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Sumar días de prórroga a fechaFin&#xa;guardar fechaProrroga y descontar 1" id="8F7osiW-PJWJIescSTIe-40">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="321" x="2750" y="5594" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Queda algún otro vencido sin devolver?" mermaidId="n:Y" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Queda algún otro vencido sin devolver?" id="8F7osiW-PJWJIescSTIe-41">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="474" width="474" x="309" y="4347" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Mantener penalización indefinida&#xa;numCaducados refleja los restantes" mermaidId="n:Y1" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Mantener penalización indefinida&#xa;numCaducados refleja los restantes" id="8F7osiW-PJWJIescSTIe-42">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="316" x="198" y="5086" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Iniciar o reiniciar castigo temporal&#xa;fechaPenalizacion = hoy" mermaidId="n:Z" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Iniciar o reiniciar castigo temporal&#xa;fechaPenalizacion = hoy" id="8F7osiW-PJWJIescSTIe-43">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="308" x="884" y="5086" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="¿Termina el plazo del castigo&#xa;y no hay nuevos vencidos?" mermaidId="n:Z1" mermaidBaseStyle="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="¿Termina el plazo del castigo&#xa;y no hay nuevos vencidos?" id="8F7osiW-PJWJIescSTIe-44">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="rhombus;html=1;strokeWidth=1;whiteSpace=wrap;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="347" width="347" x="1207" y="5457" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Sigue penalizado durante el plazo" mermaidId="n:Z2" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Sigue penalizado durante el plazo" id="8F7osiW-PJWJIescSTIe-45">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="54" width="302" x="1465" y="5916" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="Limpiar castigo&#xa;estado sin castigo" mermaidId="n:Z3" mermaidBaseStyle="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" mermaidBaseValue="Limpiar castigo&#xa;estado sin castigo" id="8F7osiW-PJWJIescSTIe-46">
          <mxCell parent="85LOYg6x6uEBZxuNiowh-0" style="html=1;whiteSpace=wrap;strokeWidth=1;fillColor=light-dark(#ECECFF,#1f2020);strokeColor=light-dark(#9370DB,#cccccc);fontColor=light-dark(#333333,#cccccc);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontSize=16;" vertex="1">
            <mxGeometry height="73" width="187" x="2479" y="5906" as="geometry" />
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:A-&gt;B#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-47">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-2" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-3">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:B-&gt;B1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.27;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-48">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-3" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.27;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-4">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1140" y="596" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:B-&gt;C#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.73;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-49">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-3" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.73;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-5">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1388" y="596" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:C-&gt;C1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.76;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-50">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-5" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.76;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-6">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1153" y="836" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:C-&gt;D#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.76;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-51">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-5" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.76;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-7">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1624" y="836" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:D-&gt;E#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-52">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-7" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-8">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:E-&gt;E1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.05;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-53">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-8" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.05;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-9">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1431" y="1368" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:E1-&gt;X#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.48;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-54">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-9" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.48;entryY=0;" target="8F7osiW-PJWJIescSTIe-10">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1431" y="1827" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:E-&gt;F#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.95;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-55">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-8" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.95;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-11">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1816" y="1368" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:F-&gt;X#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.11;exitY=1;entryX=0.85;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-56">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-11" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.11;exitY=1;entryX=0.85;entryY=0;" target="8F7osiW-PJWJIescSTIe-10">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1637" y="1827" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No; ya venció el castigo" mermaidId="e:F-&gt;F1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.62;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="No; ya venció el castigo" id="8F7osiW-PJWJIescSTIe-57">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-11" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.62;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-12">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1872" y="1827" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No; sin castigo" mermaidId="e:F-&gt;G#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.94;entryX=0.68;entryY=0;" mermaidBaseValue="No; sin castigo" id="8F7osiW-PJWJIescSTIe-58">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-11" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.94;entryX=0.68;entryY=0;" target="8F7osiW-PJWJIescSTIe-13">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2078" y="1827" />
                <mxPoint x="2078" y="1888" />
                <mxPoint x="2078" y="1940" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:F1-&gt;G#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.32;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-59">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-12" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.32;entryY=0;" target="8F7osiW-PJWJIescSTIe-13">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1872" y="1940" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:G-&gt;H#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.81;entryX=0.5;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-60">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-13" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.81;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-14">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1490" y="2063" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:H-&gt;H1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.96;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-61">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-14" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.96;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-15">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1326" y="2350" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:H-&gt;I#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.64;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-62">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-14" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.64;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-16">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2021" y="2350" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:I-&gt;J#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-63">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-16" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-17">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:J-&gt;K#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.82;entryX=0.5;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-64">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-17" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.82;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-18">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1510" y="2626" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:K-&gt;L#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.79;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-65">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-18" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.79;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-19">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1178" y="3002" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:L-&gt;AA#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.89;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-66">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-19" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.89;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-20">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="817" y="3575" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:AA-&gt;AB#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.65;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-67">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-20" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.65;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-21">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="171" y="3978" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:AB-&gt;AC#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-68">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-21" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-22">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:AA-&gt;W#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-69">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-20" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-23">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:L-&gt;AD#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.82;entryX=0.39;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-70">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-19" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.82;entryX=0.39;entryY=0;" target="8F7osiW-PJWJIescSTIe-24">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1628" y="3575" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:AD-&gt;J#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.38;entryX=1;entryY=0.84;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-71">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-24" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.38;entryX=1;entryY=0.84;" target="8F7osiW-PJWJIescSTIe-17">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2520" y="3575" />
                <mxPoint x="2520" y="3288" />
                <mxPoint x="2520" y="3002" />
                <mxPoint x="2520" y="2809" />
                <mxPoint x="2520" y="2626" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:AD-&gt;S#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.93;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-72">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-24" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.93;entryY=0;" target="8F7osiW-PJWJIescSTIe-25">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1672" y="3978" />
                <mxPoint x="1672" y="4146" />
                <mxPoint x="1672" y="4313" />
                <mxPoint x="1672" y="4584" />
                <mxPoint x="1672" y="4856" />
                <mxPoint x="1672" y="5122" />
                <mxPoint x="1672" y="5389" />
                <mxPoint x="1672" y="5630" />
                <mxPoint x="1672" y="5872" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:S-&gt;T#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-73">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-25" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-26">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:T-&gt;U#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-74">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-26" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-27">
            <mxGeometry relative="1" as="geometry">
              <Array as="points" />
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:U-&gt;U1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.69;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-75">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-27" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0.69;entryY=0;" target="8F7osiW-PJWJIescSTIe-28">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1213" y="6494" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:U1-&gt;V#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.07;entryX=0.53;entryY=1;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-76">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-28" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.07;entryX=0.53;entryY=1;" target="8F7osiW-PJWJIescSTIe-29">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="687" y="6494" />
                <mxPoint x="687" y="6306" />
                <mxPoint x="687" y="6127" />
                <mxPoint x="687" y="6066" />
                <mxPoint x="687" y="6004" />
                <mxPoint x="687" y="5943" />
                <mxPoint x="687" y="5872" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:V-&gt;S#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.47;exitY=1;entryX=0;entryY=0.02;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-77">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-29" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.47;exitY=1;entryX=0;entryY=0.02;" target="8F7osiW-PJWJIescSTIe-25">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="658" y="5872" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:V-&gt;W#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.3;entryX=0.83;entryY=1;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-78">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-29" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.3;entryX=0.83;entryY=1;" target="8F7osiW-PJWJIescSTIe-23">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1268" y="5389" />
                <mxPoint x="1268" y="5122" />
                <mxPoint x="1268" y="4856" />
                <mxPoint x="1268" y="4584" />
                <mxPoint x="1268" y="4313" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:K-&gt;M#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.68;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-79">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-18" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.68;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-30">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2056" y="3002" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:M-&gt;M1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.09;exitY=1;entryX=0.74;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-80">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-30" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.09;exitY=1;entryX=0.74;entryY=0;" target="8F7osiW-PJWJIescSTIe-31">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1822" y="3575" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:M-&gt;N#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.53;exitY=1;entryX=0.39;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-81">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-30" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.53;exitY=1;entryX=0.39;entryY=0;" target="8F7osiW-PJWJIescSTIe-32">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2074" y="3575" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:N-&gt;N1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.07;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-82">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-32" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.07;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-33">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1946" y="3978" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:N-&gt;O#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.89;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-83">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-32" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.89;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-34">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2274" y="3978" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:O-&gt;O1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.96;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-84">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-34" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0;exitY=0.96;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-35">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2094" y="4313" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:O-&gt;P#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.91;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-85">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-34" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.91;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-36">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2412" y="4313" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:P-&gt;P1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.15;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-86">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-36" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.15;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-37">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2224" y="4856" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:P-&gt;Q#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.85;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-87">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-36" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.85;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-38">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2601" y="4856" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:Q-&gt;Q1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.19;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-88">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-38" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.19;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-39">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2435" y="5389" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:Q-&gt;R#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.83;exitY=1;entryX=0.44;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-89">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-38" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.83;exitY=1;entryX=0.44;entryY=0;" target="8F7osiW-PJWJIescSTIe-40">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2777" y="5389" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:R-&gt;J#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.54;exitY=0;entryX=1;entryY=0.67;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-90">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-40" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.54;exitY=0;entryX=1;entryY=0.67;" target="8F7osiW-PJWJIescSTIe-17">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="2998" y="5389" />
                <mxPoint x="2998" y="5122" />
                <mxPoint x="2998" y="4856" />
                <mxPoint x="2998" y="4584" />
                <mxPoint x="2998" y="4313" />
                <mxPoint x="2998" y="4146" />
                <mxPoint x="2998" y="3978" />
                <mxPoint x="2998" y="3777" />
                <mxPoint x="2998" y="3575" />
                <mxPoint x="2998" y="3288" />
                <mxPoint x="2998" y="3002" />
                <mxPoint x="2998" y="2809" />
                <mxPoint x="2998" y="2626" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:W-&gt;Y#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.3;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-91">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-23" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.3;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-41">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="545" y="4313" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:Y-&gt;Y1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.15;exitY=1;entryX=0.5;entryY=0;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-92">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-41" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.15;exitY=1;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-42">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="356" y="4856" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:Y1-&gt;V#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.12;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-93">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-42" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.12;" target="8F7osiW-PJWJIescSTIe-29">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="356" y="5389" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:Y-&gt;Z#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.78;entryX=0.5;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-94">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-41" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.78;entryX=0.5;entryY=0;" target="8F7osiW-PJWJIescSTIe-43">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1038" y="4856" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:Z-&gt;Z1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.15;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-95">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-43" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.15;" target="8F7osiW-PJWJIescSTIe-44">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1038" y="5389" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="No" mermaidId="e:Z1-&gt;Z2#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.537463976945245;exitY=1;entryX=0.543046357615894;entryY=0;curved=1;exitX=0.54;exitY=1;entryX=0.54;entryY=0;" mermaidBaseValue="No" id="8F7osiW-PJWJIescSTIe-96">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-44" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.54;exitY=1;entryX=0.54;entryY=0;" target="8F7osiW-PJWJIescSTIe-45">
            <mxGeometry relative="1" as="geometry">
              <mxPoint as="offset" />
              <Array as="points">
                <mxPoint x="1543" y="5860" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:Z2-&gt;Z1#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.48013245033112584;exitY=0;entryX=0.4827089337175792;entryY=1;curved=1;exitX=0.48;exitY=0;entryX=0.48;entryY=1;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-97">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-45" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=0.48;exitY=0;entryX=0.48;entryY=1;" target="8F7osiW-PJWJIescSTIe-44">
            <mxGeometry relative="1" as="geometry">
              <mxPoint as="offset" />
              <Array as="points">
                <mxPoint x="1486" y="5860" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="Sí" mermaidId="e:Z1-&gt;Z3#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.42;" mermaidBaseValue="Sí" id="8F7osiW-PJWJIescSTIe-98">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-44" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);html=1;fontSize=16;labelBackgroundColor=light-dark(#E8E8E88D,#2a2a2a8D);fontFamily=Trebuchet MS,Verdana,Arial,sans-serif;fontColor=light-dark(#333333,#cccccc);exitX=0.5;exitY=1;entryX=0;entryY=0.42;" target="8F7osiW-PJWJIescSTIe-46">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="1381" y="5872" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
        <UserObject label="" mermaidId="e:Z3-&gt;G#0" mermaidBaseStyle="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.33;entryX=1;entryY=0.63;" mermaidBaseValue="" id="8F7osiW-PJWJIescSTIe-99">
          <mxCell edge="1" parent="85LOYg6x6uEBZxuNiowh-0" source="8F7osiW-PJWJIescSTIe-46" style="curved=1;startArrow=none;endArrow=block;endSize=7;strokeColor=light-dark(#333333,#cccccc);exitX=1;exitY=0.33;entryX=1;entryY=0.63;" target="8F7osiW-PJWJIescSTIe-13">
            <mxGeometry relative="1" as="geometry">
              <Array as="points">
                <mxPoint x="3106" y="5872" />
                <mxPoint x="3106" y="5630" />
                <mxPoint x="3106" y="5389" />
                <mxPoint x="3106" y="5122" />
                <mxPoint x="3106" y="4856" />
                <mxPoint x="3106" y="4584" />
                <mxPoint x="3106" y="4313" />
                <mxPoint x="3106" y="4146" />
                <mxPoint x="3106" y="3978" />
                <mxPoint x="3106" y="3777" />
                <mxPoint x="3106" y="3575" />
                <mxPoint x="3106" y="3288" />
                <mxPoint x="3106" y="3002" />
                <mxPoint x="3106" y="2809" />
                <mxPoint x="3106" y="2626" />
                <mxPoint x="3106" y="2564" />
                <mxPoint x="3106" y="2503" />
                <mxPoint x="3106" y="2431" />
                <mxPoint x="3106" y="2350" />
                <mxPoint x="3106" y="2202" />
                <mxPoint x="3106" y="2063" />
              </Array>
            </mxGeometry>
          </mxCell>
        </UserObject>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>

```

## Casos reflejados

- Un préstamo vencido sin devolver penaliza indefinidamente al socio.
- Si un préstamo vence mientras hay un castigo temporal, prevalece el estado indefinido.
- Con varios préstamos vencidos, devolver uno no levanta el estado indefinido mientras quede otro vencido; devolver el último inicia el castigo temporal.
- Devolver en plazo no altera un castigo temporal. Devolver tarde reinicia el castigo desde hoy si ya no quedan otros vencidos.
- Un socio penalizado no puede recibir otro préstamo. Sin penalización, puede recibirlo si el ejemplar está disponible y no se supera el límite por tipo.
- La prórroga se verifica por préstamo: solo para un préstamo activo, no vencido, de un socio no penalizado y con prórrogas disponibles. Cada prórroga suma los días configurados a la fecha de fin actual.
- La fecha de fin igual a hoy todavía no se considera vencida; la caducidad se produce cuando `fechaFin < hoy`.

Los valores por defecto (si no se sobrescriben por configuración) son: préstamo de 20 días, 3 prórrogas de 5 días cada una, castigo de 1 día y límites activos de 3 libros, 2 grabaciones y 1 revista. Están definidos en `prestamos.models`.
