/*
Add meal to localStorage
param id: meal id
param name: meal name
param price: meal price
*/
function add_meal(id, name, price) {
    var meals = JSON.parse(localStorage.meals ? localStorage.meals : '[]');

    // check if the meal is in the cart
    var is_new_meal = true;
    for (var i = 0; i < meals.length; i++) {
        if (meals[i]['id'] == id) {
            meals[i]['amount'] += 1;
            is_new_meal = false;
            break;
        }
    }

    if (is_new_meal) {
        meals.push({
            id : id,
            amount : 1,
            price : price,
            name : name
        });
    }
    localStorage.meals = JSON.stringify(meals);
}

/*
Delete meal in the localStorage
param id: meal id
*/
function delete_meal(id) {
    var meals = JSON.parse(localStorage.meals ? localStorage.meals : '[]');
    for (var i = 0; i < meals.length; i++) {
        if (meals[i]['id'] == id) {
            meals.splice(i, 1);
            break;
        }
    }
    localStorage.meals = JSON.stringify(meals);
}

/*
Minus meal from localStorage
param id: meal id
param amount: meal count to minus. Default 1
*/
function minus_meal(id, amount) {
    amount = amount || 1;
    var meals = JSON.parse(localStorage.meals ? localStorage.meals : '[]');
    var result = 0;
    for (var i = 0; i < meals.length; i++) {
        if (meals[i]['id'] == id) {
            meals[i]['amount'] -= amount;
            if (meals[i]['amount'] < 0) {
                meals[i]['amount'] = 0;
            }
            result = meals[i]['amount'];
            break;
        }
    }
    localStorage.meals = JSON.stringify(meals);
    return result;
}

/*
Plus meal in the localStorage
param id: meal id
param amount: meal count to plus. Default 1
*/
function plus_meal(id, amount) {
    amount = amount || 1;
    var meals = JSON.parse(localStorage.meals ? localStorage.meals : '[]');
    for (var i = 0; i < meals.length; i++) {
        if (meals[i]['id'] == id) {
            meals[i]['amount'] += amount;
            break;
        }
    }
    localStorage.meals = JSON.stringify(meals);
}

/*
Get all meals from localStorage.
return a JSON object with meals, total price and total amount.
*/
function get_meals() {
    var meals = JSON.parse(localStorage.meals ? localStorage.meals : '[]');
    var total_amount = 0;
    var total_price = 0;
    for (var i = 0; i < meals.length; i++) {
        meals[i]['subtotal'] = meals[i]['amount'] * meals[i]['price'];
        total_amount += meals[i]['amount'];
        total_price += meals[i]['subtotal'];
    }
    return {
        meals: meals,
        total: {
            price: total_price,
            amount: total_amount
        }
    };
}

// clear the meals in the localStorage
function clear_meals() {
    localStorage.meals = JSON.stringify([]);
}
