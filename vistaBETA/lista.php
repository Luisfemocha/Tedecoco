<?php
$clientes = array(
    array("Ricardo","1234", "19"),
    array("José","11212","23"),
    array("Alex","123123","20"),
    array("Manuela","66456","25"),
    array("Maria","66789","19"),
    array("Juan","45535","20"),
    array("Luis","008678","19"),
);
?>

<head>
    <meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel = "stylesheet" href = "style.scss">
	
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
	<title>LEER</title>
</head>
<body class="cuerpo">
	<header>
    </header>
    <main>
		<table class="table table-bordered">
			<thead>
				<tr>
				<th scope="col" class="textoPrincipal">NOMBRE</th>
				<th scope="col" class="textoPrincipal">CLAVE</th>
				<th scope="col" class="textoPrincipal">EDAD</th>
				</tr>
			</thead>
			<tbody>
				<?php foreach($clientes as $valor):?>
				<tr>
						<td class="textoPrincipal"><?php echo($valor[0]) ?></td>
						<td class="textoPrincipal"><?php echo($valor[1]) ?></td>
						<td class="textoPrincipal"><?php echo($valor[2]) ?></td>
						<td class="textoPrincipal">
							<a href="modificar.php" class="btn btn-primary">Modificar</a>
							<a href="#" class="btn btn-danger">Eliminar</a>
						</td>
				</tr>
				<?php endforeach?>
			</tbody>
		</table>
    </main>
    <footer>
    <p>REALIZADO POR:<br>
        Luis Felipe Moreno Chamorro<br>
        Kevin Danilo Arias Buitrago<br>
        Michael Stiwar Zapata Agudelo<br>
        Juan José Hurtado Álvarez<br>
        Julian Esteban Carvajal<br>
        Federico Milotta<br>
        Juan Felipe Valencia<br>
        <br>
        Teoría de la computación y compilación
        Universidad Nacional de Colombia sede Medellín 2020
    </p>
    </footer>
    <script src="https://kit.fontawesome.com/2c36e9b7b1.js" crossorigin="anonymous"></script>
	<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>

</body>