document.addEventListener("DOMContentLoaded", function() {
    // Delay the loading circle for 10 seconds (10000 milliseconds)
    setTimeout(function() {
        document.querySelector('.loading-overlay').style.display = 'none';
        document.querySelector('.loading-page').classList.add('active'); // Add this line
    }, 10000); // 10000 milliseconds (10 seconds)

    setTimeout(function() {
            document.querySelectorAll('.loading-dot').forEach(function(dot) {
                 dot.style.animation = 'none'; // Stop the animation
             });
         }, 10000); 
         setTimeout(function() {
            document.querySelectorAll('.loading-dot1').forEach(function(dot) {
                 dot.style.animation = 'none'; // Stop the animation
             });
         }, 20000); 
         setTimeout(function() {
            document.querySelectorAll('.loading-dot2').forEach(function(dot) {
                 dot.style.animation = 'none'; // Stop the animation
             });
         }, 30000); 
         
    // Delay the logo arrival for 30 seconds after the loading circle disappears
    setTimeout(function() {
        // Show the logo container
        document.querySelector('.logo-container').classList.add('active');
    }, 10000); // 30000 milliseconds (30 seconds)

    document.querySelector('.logo').addEventListener('click', function() {
        window.location.href = 'form.html';
    });
});