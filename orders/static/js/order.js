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
    });

    // create order
    $('#create-order-btn').click(function(){
        var btn = $(this);
        var meals = get_meals().meals;
        var building = $('#building').val();
        var location = $('#location').val();

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
                csrfmiddlewaretoken: get_cookie('csrftoken')
            },
            success: function(result) {
                clear_meals();
                btn.button('reset');
                window.location.href = result.success_url;
            }
        });
    });
});
