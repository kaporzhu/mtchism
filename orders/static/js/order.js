$(document).ready(function(){
    // load selected meals from localStorage
    function load_meals() {
        var meals = get_meals();
        if (meals.meals.length == 0) {
            window.location.href = $('#back-to-meals-btn').attr('href');
        }

        $('#selected-meals tr').remove();
        var ractive = new Ractive({
            el: 'selected-meals',
            template: '#selected-meal-template',
            data: meals
        });
    }
    load_meals();

    // plus or minus meal amount
    $(document).on('click', '.plus-meal', function(){
        plus_meal($(this).data('id'));
        load_meals();
    });
    $(document).on('click', '.minus-meal', function(){
        var id = $(this).data('id');
        var amount = minus_meal(id);
        if (amount == 0) {
            if (confirm('要删除这个套餐吗？')) {
                delete_meal(id);
                $(this).parents('tr').remove();
            } else {
                return false;
            }
        }
        load_meals();
        update_deliver_time_selector();
    });

    // remove meal type checkbox not checked wanring
    $('.meal-type-checkbox').change(function(){
        $(this).parents('td').removeClass('alert-danger');
    });

    // create order
    $('#create-order-btn').click(function(){
        var btn = $(this);
        var meals = get_meals().meals;
        var building = $('#building').val();
        var location = $('#location').val();
        var breakfast_deliver_time = $('#breakfast-deliver-time-select:not(.hidden) select').val();
        var lunch_deliver_time = $('#lunch-deliver-time-select:not(.hidden) select').val();
        var supper_deliver_time = $('#supper-deliver-time-select:not(.hidden) select').val();

        // update selected meal type
        var all_meal_type_selected = true;
        for (var i=0; i<meals.length; i++) {
            var meal = meals[i];
            var meal_type = $('input[name=meal-type-{id}]:checked'.replace('{id}', meal.id)).val();
            if (!meal_type) {
                $('#meal-{id} .meal-type'.replace('{id}', meal.id)).addClass('alert-danger');
                all_meal_type_selected = false;
            } else {
                meal.meal_type = meal_type;
            }
        }
        if (!all_meal_type_selected) {
            alert('我们还不知道您想什么时候吃，选一下早餐、午餐还是晚餐吧');
            return;
        }

        if (location.length < 5) {
            alert('地址不够具体，我们的配送小哥会抓狂的。');
            return;
        }

        btn.button('loading');
        $.ajax({
            url: '.',
            type: 'post',
            dataType: 'json',
            data: {
                meals: JSON.stringify(meals),
                building: building,
                location: location,
                breakfast_deliver_time: breakfast_deliver_time,
                lunch_deliver_time: lunch_deliver_time,
                supper_deliver_time: supper_deliver_time,
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            success: function(result) {
                clear_meals();
                btn.button('reset');
                window.location.href = result.success_url;
            }
        });
    });

    // check all selected meals, hide breakfast deliver time selector if there's not breakfast food
    function update_deliver_time_selector() {
        var meals = get_meals().meals;
        var time_selector = {
            breakfast: false,
            lunch: false,
            supper: false
        };
        var breakfast = false, lunch = false; supper = false;
        for (var i=0; i<meals.length; i++) {
            var limitations = meals[i].limitations;
            for (var j=0; j<limitations.length; j++) {
                for (var type in time_selector) {
                    if (type == limitations[j].type) {
                        time_selector[type] = true;
                    }
                }
            }
        }

        for (var type in time_selector) {
            if (!time_selector[type]) {
                $('#{type}-deliver-time-select'.replace('{type}', type)).addClass('hidden');
            } else {
                $('#{type}-deliver-time-select'.replace('{type}', type)).removeClass('hidden');
            }
        }
    }
    update_deliver_time_selector();
});
