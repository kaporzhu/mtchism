$(document).ready(function(){
    // hightlight the checked meal
    $('.panel .list-group-item input').change(function(){
        if ($(this).is(':checked')) {
            $(this).parents('.list-group-item').addClass('active');
        } else {
            $(this).parents('.list-group-item').removeClass('active');
        }
        update_selected_meals();
    });

    function get_selected_meals() {
        var selected_meals = [];
        $('.panel .list-group-item input:checked').each(function(){
            var $input = $(this);
            selected_meals.push({
                'id': $input.val(),
                'category': $input.data('category'),
                'name': $input.data('name'),
                'price': $input.data('price'),
                'meal_type': $input.data('type'),
            });
        });
        return selected_meals;
    }

    function update_selected_meals() {
        var selected_meals = get_selected_meals();
        // clear the selected meals
        $('#selected-meals').empty();
        $.each(selected_meals, function(){
            var text = '{category}: {name} [{price}]'.replace('{category}', this.category).replace('{name}', this.name).replace('{price}', this.price);
            $('#selected-meals').append($('<li class="list-group-item">').text(text));
        });
    }

    // checkbox
    $('#checkbox').click(function(){
        var selected_meals = get_selected_meals();
        localStorage.stage_meals = JSON.stringify(selected_meals);
        location.href = $(this).data('url');
    });
});
