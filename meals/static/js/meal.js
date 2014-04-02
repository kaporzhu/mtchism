$(document).ready(function(){

    // add food to the dish
    $('#add-dishfood-btn').click(function(){
        var food_id = $('#food-id').val();
        var food_name = $('#food-name').val();
        var food_weight = $('#food-weight').val();
        var $dish_foods = $('#dish-foods');
        var food_item_tmpl =
            '<li data-id="{id}" data-weight="{weight}">' +
                '{name}: {weight}' +
                '<a class="remove-food-btn" href="javascript:void(0)" data-dishfood-id="{id}">' +
                    '<span class="glyphicon glyphicon-remove"></span>' +
                '</a>' +
            '</li>';
        $dish_foods.append(food_item_tmpl.replace(/{name}/g, food_name).replace(/{id}/g, food_id).replace(/{weight}/g, food_weight));
        update_dish_foods();
    });

    // remove the food from dish
    $(document).on('click', 'a.remove-food-btn', function(){
        $(this).parents('li').remove();
        update_dish_foods();
    });

    // bind autocomplete for the food name field
    $('#food-name').autocomplete({
      source: $('#food-name').data('ajax-url'),
      minLength: 1,
      select: function(event, ui) {
          $('#food-id').val(ui.item.id);
      }
    });

    // update dish foods info in the hidden field
    function update_dish_foods() {
        var foods = [];
        $('#dish-foods li').each(function(){
            foods.push({
                'dishfood_id': $(this).data('dishfood-id'),
                'id': $(this).data('id'),
                'weight': $(this).data('weight')
            });
        });
        $('#id_foods').val(JSON.stringify(foods));
    }
    update_dish_foods();
});
