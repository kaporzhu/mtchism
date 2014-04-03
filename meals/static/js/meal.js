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
    if ($('#food-name').size()) {
        $('#food-name').autocomplete({
          source: $('#food-name').data('ajax-url'),
          minLength: 1,
          select: function(event, ui) {
              $('#food-id').val(ui.item.id);
          }
        });
    }

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

    // toggle meal details in the meal index page
    $('.list-group-item').click(function(){
        $(this).children('.details').toggleClass('hidden');
        $(this).children('.dishes').toggleClass('hidden');
    });

    // add to cart
    $('.add-to-cart').click(function(event){
        $('#selected-meals').removeClass('hidden');
        var id = $(this).data('id');
        var name = $(this).data('name');
        var price = parseFloat( $(this).data('price'));

        // check if the meal is in the cart
        if ($('#meal_'+id).size()) {
            var $meal_item = $('#meal_'+id);
            var amount = parseInt($meal_item.find('.amount').text());
            $meal_item.find('.amount').text(amount+1);
            $meal_item.find('.subtotal').text((amount+1)*price);
        } else {
            var item_tmpl =
                '<li class="list-group-item meal" id="meal_{id}">' +
                    '<b>{name}</b> x <span class="amount">1</span> = <span class="subtotal">{subtotal}</span>' +
                    '<a href="javascript:void(0)" class="remove-selected-meal">x</a>' +
                '</li>';
            $('#selected-meals .last').before(item_tmpl.replace(/{name}/g, $(this).data('name')).replace(/{id}/g, $(this).data('id')).replace(/{subtotal}/g, price));
        }
        update_total_price();
        return false;
    });

    $(document).on('click', '.remove-selected-meal', function(){
        $(this).parents('li').remove();
        update_total_price();
        if ($('#selected-meals .meal').size() == 0) {
            $('#selected-meals').addClass('hidden');
        }
    });

    // update total price in the shopping cart
    function update_total_price() {
        var total = 0;
        $('#selected-meals').children('.meal').each(function(){
            total += parseFloat($(this).find('.subtotal').text());
        });
        $('#selected-meals .total').text(total);
    }

});
