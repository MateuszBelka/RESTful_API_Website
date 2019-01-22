
  $( document ).ready(function() {
    getDatabase();
  });

  function sortTable(n, tableClass) {
    var table, rows, switching, i, x, y, shouldSwitch, switchcount = 0;
    table = document.getElementsByClassName(tableClass)[0];
    switching = true;
    while (switching) {
      switching = false;
      rows = table.rows;
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        if (x.innerHTML.toString().toLowerCase() > y.innerHTML.toString().toLowerCase()) {
          shouldSwitch= true;
          break;
        }
      }
      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        switchcount ++;
      }
    }
  }

  function resetDatabase() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "https://wt.ops.labs.vu.nl/api19/bc9041de/reset", true); //http://localhost:8080/reset
    xhttp.send();
    getDatabase();
  }

  function getDatabase() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function()  {
      if (this.readyState == 4 && this.status == 200) {
        var jsonResponse = JSON.parse(this.responseText);
        putJSONinTable(jsonResponse);
      }
    }
    xhttp.open("GET","https://wt.ops.labs.vu.nl/api19/bc9041de",true);  //http://localhost:8080/
    xhttp.send();
  }

  function putJSONinTable(data) {
    var table = "";
    var count = Object.keys(data).length;
    for (var i = 0; i < count; i++) {
      table += "<tr><td>" + data[i].product + "</td><td>" + data[i].origin +
      "</td><td>" + data[i].best_before_date + "</td><td>" + data[i].amount +
      "</td><td><figure><img src="	+ data[i].image + " width=150 height=150 ></figure></td></tr>";
    }
    document.getElementById("body").innerHTML = table;
  }

  function submitFunction() {
    var product = $("#product").val();
    var origin = $("#origin").val();
    var best_before_date = $("#best_before_date").val();
    var amount = $("#amount").val();
    var image = $("#image").val();
    var formData = {product: product, origin: origin, best_before_date: best_before_date, amount: amount, image: image};
    if( product && origin && best_before_date && amount && image){
    }else{
      alert("Please fill in all fields");
      event.preventDefault();
      return;
    }
    $.ajax({
      url: 'https://wt.ops.labs.vu.nl/api19/bc9041de', //
      type: "POST",
      contentType: 'application/json',
      data: JSON.stringify(formData),
      complete: function(){
        document.forms['my_form'].reset()
      }
    });
    $('table').find('#body').append("<tr><td>" + product + "</td><td>" + origin +
    "</td><td>" + best_before_date + "</td><td>" + amount +
    "</td><td><figure><img src="	+ image + " width=150 height=150 ></figure></td></tr>");
    event.preventDefault();
  }
