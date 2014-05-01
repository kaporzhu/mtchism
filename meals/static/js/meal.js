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
        var id = $(this).data('id');
        var name = $(this).data('name');
        var limitations = $(this).data('limitations');

        var price = parseFloat( $(this).data('price'));
        add_meal(id, name, price, limitations);
        load_meals();
        return false;
    });

    $(document).on('click', '.delete-meal', function(){
        var id = $(this).parents('li').data('id');
        delete_meal(id);
        load_meals();
    });
    $(document).on('click', '.minus-meal', function(){
        var id = $(this).parents('li').data('id');
        var amount = minus_meal(id);
        if (amount == 0) {
            delete_meal(id);
            $(this).parents('li').remove();
        }
        load_meals();
    });
    $(document).on('click', '.plus-meal', function(){
        var id = $(this).parents('li').data('id');
        plus_meal(id);
        load_meals();
    });

    // load selected meals from localStorage
    function load_meals() {
        var meals = get_meals();
        var checkout_url = $('#selected-meals').data('checkout-url');
        meals['checkout_url'] = checkout_url;
        $('#selected-meals li').remove();
        if (meals.meals.length > 0){
            $('#selected-meals').removeClass('hidden');
        } else {
            $('#selected-meals').addClass('hidden');
        }
        var ractive = new Ractive({
            el: '#selected-meals',
            template: '#selected-meal-template',
            data: meals
        });
    }
    load_meals();
});
