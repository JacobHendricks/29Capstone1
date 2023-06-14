document.getElementById('date').valueAsDate = new Date();

$("#favorites-list").on("click", ".unfavor-button", async function (evt) {
  evt.preventDefault();
  let $food = $(evt.target).closest("tr");
  let foodId = $food.attr("data-food-id");

  await axios.patch(`https://nutrition-tracker-sfqe.onrender.com/api/foods/favorite/${foodId}`);
  
  $food.remove();
});