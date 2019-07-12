$(document).ready(function() {
  // For production dashboard
  $('#startProduction').on('click', function(){
    $('#startProduction').toggleClass('btn-danger');
    if ($('#startProduction').hasClass('btn-danger')){
      socket.emit("production", {on: true});
      $('#startProduction').html("Stop &nbsp; <i class='fas fa-stop fa-sm text-white'></i>");
    }
    else {
      socket.emit("production", {on: false});
      $('#startProduction').html("Start &nbsp; <i class='fas fa-play fa-sm text-white'></i>");
    }
  });

  socket.on('sample rate', function(data){
      
      if(data['sample rate'] > 250*1.15 || data['sample rate'] < 250*0.85 ){
          $('#sampleRate').css('background-color', 'red');
          $('#sampleRate').css('border-color', 'red');
      }
      else{
          $('#sampleRate').css('background-color', 'grey');
          $('#sampleRate').css('border-color', 'grey');
      }
      $('#sampleRate').html(data['sample rate'] + " hz");
      console.log('SAMPLE RATE RECEIVED OF : ' + data['sample rate']);
    });
});
