document.getElementById('date').valueAsDate = new Date();

$("#favorites-list").on("click", ".unfavor-button", async function (evt) {
  evt.preventDefault();
  let $food = $(evt.target).closest("tr");
  let foodId = $food.attr("data-food-id");

  await axios.patch(`http://127.0.0.1:5000/api/foods/favorite/${foodId}`);
  
  $food.remove();
});