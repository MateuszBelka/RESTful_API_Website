//Populate the table when website loads
$( document ).ready(function() {
    getDatabase();
});

//Algorithm for sorting table
//Works on the principle of bubble sort
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

//Receiving information from database about the table contents
function getDatabase() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function()  {
    if (this.readyState == 4 && this.status == 200) {
      var jsonResponse = JSON.parse(this.responseText);
      putJSONinTable(jsonResponse);
    }
  }
  xhttp.open("GET","http://localhost:8080/retrieve",true);
  xhttp.send();
}

//Populating table with recieved data
function putJSONinTable(data) {
  var table = "";
  var count = Object.keys(data).length;
  for (var i = 0; i < count; i++) {
    table += "<tr><td>" + data[i].product + "</td><td>" + data[i].origin +
    "</td><td>" + data[i].best_before_date + "</td><td>" + data[i].amount +
    "</td><td><figure><img src=" + data[i].image + " width=150 height=150 ></figure></td></tr>";
  }
  document.getElementById("body").innerHTML = table;
}

//Creating new item in the database
function submitFunction() {
  //Taking information from form and keeping it as a variable
  var product = $("#product").val();
  var origin = $("#origin").val();
  var best_before_date = $("#best_before_date").val();
  var amount = $("#amount").val();
  var image = $("#image").val();
  var formData = {product: product, origin: origin, best_before_date: best_before_date, amount: amount, image: image};
  if( product && origin && best_before_date && amount && image){
  }else{
    //If there is missing information in the form
    alert("Please fill in all fields");
    event.preventDefault();
    return;
  }
  $.ajax({
    url: 'http://localhost:8080/create',
    type: 'POST',
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

//Updating an item in the database
function updateFunction() {
  //Taking information from form and keeping it as a variable
  var product = $("#product").val();
  var origin = $("#origin").val();
  var best_before_date = $("#best_before_date").val();
  var amount = $("#amount").val();
  var image = $("#image").val();
  var id = $("#id").val();
  var formData = {product: product, origin: origin, best_before_date: best_before_date, amount: amount, image: image, id: id};
  if( product && origin && best_before_date && amount && image && id){
  }else{
    //If there is missing information in the form
    alert("Please fill in all fields");
    event.preventDefault();
    return;
  }
  $.ajax({
    url: 'http://localhost:8080/update/' + id,
    type: "PUT",
    contentType: 'application/json',
    data: JSON.stringify(formData),
    complete: function(){
      document.forms['my_form'].reset()
    }
  });
  getDatabase();
  event.preventDefault();
}

//Deleting specific item in the database
function deleteFunction() {
  //Taking information from form and keeping it as a variable
  var id = $("#id").val();
  if(id){
  }else{
    //If there is missing information in the form
    alert("Please fill in all fields");
    event.preventDefault();
    return;
  }
  $.ajax({
    url: 'http://localhost:8080/delete/' + id,
    type: 'DELETE',
    complete: function(){
      document.forms['my_form'].reset()
    }
  });
  getDatabase();
  event.preventDefault();
}
