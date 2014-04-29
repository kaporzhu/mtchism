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
            data: meals,
            complete: function() {
                update_deliver_time_selector();
            }
        });
    }

    function load_stage_meals() {
        var meals = JSON.parse(localStorage.stage_meals);
        var total_amount = 0;
        var total_price = 0;
        $.each(meals, function(){
            total_amount += 1;
            total_price += parseFloat(this.price);
        });

        $('#selected-stage-meals tr').remove();
        var ractive = new Ractive({
            el: 'selected-stage-meals',
            template: '#selected-stage-meal-template',
            data: {meals: meals, total: {price: total_price, amount: total_amount}},
            complete: function() {
                update_deliver_time_selector();
            }
        });
    }

    if ($('#selected_stage_meals').size() > 0) {
        load_stage_meals();
    } else if ($('#selected_meals').size() > 0) {
        load_meals();
    }

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
        update_deliver_time_selector();
    });

    // hide or show deliver time selectors
    function update_deliver_time_selector() {
        var time_selector = {
            breakfast: false,
            lunch: false,
            supper: false
        };
        $('#selected-meals .meal-type').each(function(){
            var $checked_input = $(this).find('input:checked');
            if ($checked_input.size() > 0) {
                time_selector[$checked_input.val()] = true;
            } else {
                $(this).find('input').each(function(){
                    time_selector[$(this).val()] = true;
                });
            }
        });

        $('#selected-stage-meals .meal-type').each(function(){
            var type = $(this).data('type');
            if (type in time_selector) {
                time_selector[type] = true;
            }
        });

        for (var type in time_selector) {
            if (!time_selector[type]) {
                $('#{type}-deliver-time-select'.replace('{type}', type)).addClass('hidden');
            } else {
                $('#{type}-deliver-time-select'.replace('{type}', type)).removeClass('hidden');
            }
        }
    }

    // create order
    $('#create-order-btn').click(function(){
        if ($('#selected_stage_meals').size() > 0) {
            var meals = JSON.parse(localStorage.stage_meals);
        } else if ($('#selected_meals').size() > 0) {
            var meals = get_meals().meals;
        }
        var $btn = $(this);
        var building = $('#building').val();
        var location = $('#location').val();
        var breakfast_deliver_time = $('#breakfast-deliver-time-select:not(.hidden) select').val();
        var lunch_deliver_time = $('#lunch-deliver-time-select:not(.hidden) select').val();
        var supper_deliver_time = $('#supper-deliver-time-select:not(.hidden) select').val();

        if ($('#selected_meals').size() > 0) {
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
        }

        if (location.length < 5) {
            alert('地址不够具体，我们的配送小哥会抓狂的。');
            return;
        }

        $btn.button('loading');
        $.ajax({
            url: $btn.data('url'),
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
                $btn.button('reset');
                window.location.href = result.success_url;
            }
        });
    });
});
