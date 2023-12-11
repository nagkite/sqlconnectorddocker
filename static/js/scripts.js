document.getElementById('correct_sql').addEventListener('click', function() {
    sendSQL('correct');
  });
  
  document.getElementById('explain_sql').addEventListener('click', function() {
    sendSQL('explain');
  });
  
  function sendSQL(action) {
    var form = document.getElementById('sqlForm');
    var formData = new FormData(form);
    formData.append('action', action); // Append the action to the form data
  
    var feedbackElement = document.getElementById('feedback');
    var resultElement = document.getElementById('result');
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/process_sql', true);
    xhr.onload = function() {
      feedbackElement.textContent = ''; // Clear previous feedback
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        resultElement.innerHTML = response.result; // Display the result
        feedbackElement.textContent = action.charAt(0).toUpperCase() + action.slice(1) + 'ed Successfully!';
      } else {
        feedbackElement.textContent = 'Error: ' + xhr.statusText;
      }
    };
    xhr.send(formData);
  }
  