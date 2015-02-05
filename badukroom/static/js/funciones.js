/**
 * 
 

$.holaMundo=function(){
	alert("Hola Mundo");
}



$.aceptarPeticion=function(){
	$('#aceptar').on('click', function(event) {
		event.preventDefault();
		alert("entramos en aceptarPeticion");
		alert($('#nick').text());
		$.post("{% url 'redsocial:aceptar_peticion' %}",{ nick: $('#nick').text() }, function(data){
			alert('Vamos a recargar porque fue un exito')
			//location.reload(true);
			
				html="";
				html+="<div class='modal-body'> <p>"+data+"</p></div>";
				$('#modal').html(html);
			 

			html="<a id='#' href='#' class='btn btn-info' role='button'>Eliminar amigo</a>";
			$('#botones').html(html);

			$("#aceptar_peticion").modal('show'); 


		});
	});
}

$.declinarPeticion=function(){
	$('#rechazar').on('click', function(event){
		event.preventDefault();
		alert("entramos en borrarPeticion");
		alert($('#nick').text());
		$.get("{% url 'redsocial:declinar_peticion' %}", {nick: $('#nick').text() }, function(data){
			alert('Vamos a recargar porque se borró con exito');
			location.reload(true);
		});
	});
}


$('#formulario').submit(function(event) { // catch the form's submit event
	event.preventDefault();
	$.ajax({ // create an AJAX call...
		data: $(this).serialize(), // get the form data
		type: $(this).attr('method'), // GET or POST
		url: $(this).attr('action'), // the file to call
		success: function(data){ // on success..
			console.log("comentario creado");
			console.log(data);
			console.log("recargando página");
			location.reload(true);

		}  
	});

});


$.comentar=function(){
	$('#formulario').submit(function(event) { // catch the form's submit event
		event.preventDefault();
		$.ajax({ // create an AJAX call...
			data: $(this).serialize(), // get the form data
			type: $(this).attr('method'), // GET or POST
			url: $(this).attr('action'), // the file to call
			success: function(data){ // on success..
				console.log("comentario creado");
				console.log(data);
				console.log("recargando página");
				location.reload(true);

			}  
		});
	});
}


$('#buscar').on('click', function(event) { // catch the form's submit event
	event.preventDefault();
	alert($('#buscar_texto').val())

	$.ajax({ // create an AJAX call...
		data: {"texto":$('#buscar_texto').val()}, // get the form data
		type: 'POST', // GET or POST
		url: "{% url 'redsocial:buscar' %}", // the file to call
		success: function(data){ // on success..
			console.log(data);
			console.log("construyendo enlaces");
			html=""
				for(var i=0;i<data.length; i++){
					console.log(data[i]);
					console.log(data[i].username);
					html+="<a href='/redsocial/"+data[i].username+"' class='list-group-item'>"+data[i].first_name+" "+data[i].last_name+"</a>"
				}
			$('#list-group').html(html)
			window.location("{ url 'redsocial:{username}' }"); 
		}  
	});

});


$.buscador=function(){
	$('#buscar').on('click', function(event) { // catch the form's submit event
		event.preventDefault();
		alert($('#buscar_texto').val())

		$.ajax({ // create an AJAX call...
			data: {"texto":$('#buscar_texto').val()}, // get the form data
			type: 'POST', // GET or POST
			url: "{% url 'redsocial:buscar' %}", // the file to call
			success: function(data){ // on success..
				console.log(data);
				console.log("construyendo enlaces");
				html=""
					for(var i=0;i<data.length; i++){
						console.log(data[i]);
						console.log(data[i].username);
						html+="<a href='/redsocial/"+data[i].username+"' class='list-group-item'>"+data[i].first_name+" "+data[i].last_name+"</a>"
					}
				$('#list-group').html(html)
				//window.location("{ url 'redsocial:{username}' }"); 
			}  
		});
	});
}

$('#agregar').on('click', function(event){
	event.preventDefault();
	var perfil=$('#nick').text();
	console.log(perfil);
	alert($('#nick').text());
	$.ajax({
		data:{"perfil_para_agregar":perfil},
		type:'POST',
		url: "{% url 'redsocial:agregar_ajax' %}",
		success: function(data){
			var perfil=$('#nick').text();
			html="<a id='#' href='#' class='btn btn-info' role='button'>La peticion ya ha sido enviada</a>";
			$('#botones').html(html);

			$("#example").modal('show'); 



			console.log(perfil);
			console.log(data);
		}
	});
});


$.agregar=function(){
	$('#agregar').on('click', function(event){
		event.preventDefault();
		var perfil=$('#nick').text();
		console.log(perfil);
		alert($('#nick').text());
		$.ajax({
			data:{"perfil_para_agregar":perfil},
			type:'POST',
			url: "{% url 'redsocial:agregar_ajax' %}",
			success: function(data){
				var perfil=$('#nick').text();
				html="<a id='#' href='#' class='btn btn-info' role='button'>La peticion ya ha sido enviada</a>";
				$('#botones').html(html);
				$("#example").modal('show'); 
				console.log(perfil);
				console.log(data);
			}
		});
	});
}


$.limpiar=function(boton){
	$.get("{% url 'redsocial:limpiar_notificaciones' %}", {boton: boton}, function(data){
		
		//location.reload(true);
		
		setTimeout(function(){location.reload()},2000);
	});
}

$.limpiarNotificaciones=function(){
	$('#limpiar_notificaciones').on('click', function(event){
		event.preventDefault();
		var boton='limpiar_notificaciones';
		$.limpiar(boton);
		$('#notificar').html("Se eliminaron correctamente las notificaciones");
	});
}

$.limpiarPeticiones=function(){
	$('#limpiar_peticiones').on('click', function(event){
		event.preventDefault();
		var boton='limpiar_peticiones';
		$.limpiar(boton);
		$('#peticion').html("Se eliminaron correctamente las peticiones");
	});
}

*/
