document.getElementById('date').valueAsDate = new Date();

dailyTotal = {
  calories: 0, 
  carbs: 0, 
  protein: 0, 
  fat: 0
};

dailyRemaining = {
  calories: 150, 
  carbs: 20, 
  protein: 50, 
  fat: 40
};

function generateMealHTML(food) {
  return `
    <tr data-food-id=${food.id}>
      <td><img src="${food.img}" alt="IMG" class="img-fluid"></td>
      <td>${food.food_name}</td>
      <td>${food.serving_qty}</td>
      <td>${food.serving_unit}</td>
      <td>${Math.round(food.calories)}</td>
      <td>${Math.round(food.carbs)}</td>
      <td>${Math.round(food.protein)}</td>
      <td>${Math.round(food.total_fat)}</td>
      <td><button class="delete-button button btn btn-outline-danger btn-sm">x</button></td>
    </tr>
  `;
}


async function refresh() {
  // Pull all food data from DB for the selected date. Display foods by meal on homepage and update daily totals table.

  let date = $("#date").val();
  dailyTotal.calories = 0;
  dailyTotal.carbs = 0;
  dailyTotal.protein = 0;
  dailyTotal.fat = 0;
  
  for (let meal of ["breakfast", "lunch", "dinner", "snacks"]) {
    $(`#${meal}-table-body`).empty();
    const response = await axios.get(`https://nutrition-tracker-sfqe.onrender.com/api/foods/${meal}/${date}`);
    console.log(meal)
    console.log("FOOD LIST", response.data)
    // show the table only if there is food for that meal
    if (response.data.food_list.length) {
      $(`#${meal}-container`).show(); 
    }
    else {
      $(`#${meal}-container`).hide();
    }
    // Add food data to meal table
    for (let mealData of response.data.food_list) {
      let newFood = $(generateMealHTML(mealData));
      $(`#${meal}-table`).append(newFood);
      addTotal(mealData);
    }
  }
  updateDailyTotal();
};


function addTotal(food) {
  dailyTotal.calories += food.calories;
  dailyTotal.carbs += food.carbs;
  dailyTotal.protein += food.protein;
  dailyTotal.fat += food.total_fat;
}

function updateDailyTotal() {
  $("#cal-consumed").text(Math.round(dailyTotal.calories));
  $("#cal-remaining").text(Math.round(parseFloat($("#cal-goal").text()) - dailyTotal.calories));
  $("#carb-consumed").text(Math.round(dailyTotal.carbs));
  $("#carb-remaining").text(Math.round(parseFloat($("#carb-goal").text()) - dailyTotal.carbs));
  $("#protein-consumed").text(Math.round(dailyTotal.protein));
  $("#protein-remaining").text(Math.round(parseFloat($("#protein-goal").text()) - dailyTotal.protein));
  $("#fat-consumed").text(Math.round(dailyTotal.fat));
  $("#fat-remaining").text(Math.round(parseFloat($("#fat-goal").text()) - dailyTotal.fat));
}


// on date selection
$("#date").on("change", function(evt) {
  evt.preventDefault();
  refresh();
})

// on page load
$().ready(() => {
  refresh();
});

// handle clicking delete: delete food and consumed record
$("#food-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();
  let $food = $(evt.target).closest("tr");
  let foodId = $food.attr("data-food-id");
  let date = $("#date").val();

  await axios.delete(`https://nutrition-tracker-sfqe.onrender.com/api/foods/${foodId}/${date}`);
  $food.remove();
  refresh();
});
