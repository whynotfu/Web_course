const dishes = [
  // ===== SOUPS =====
  {
    keyword: "chicken_soup",
    name: "Chicken soup with noodles",
    price: 350,
    category: "soup",
    kind: "meat",
    count: "350 g",
    image: "png/chickenSoop.jfif"
  },
  {
    keyword: "borsh",
    name: "Classic borsh with sour cream",
    price: 360,
    category: "soup",
    kind: "meat",
    count: "380 g",
    image: "png/borsh.jfif"
  },
  {
    keyword: "vegetable_soup",
    name: "Vegetable soup with lentils and herbs",
    price: 320,
    category: "soup",
    kind: "veg",
    count: "340 g",
    image: "png/Vegetablesoup.jfif"
  },
  {
  keyword: "tomato_soup",
  name: "Tomato soup with basil",
  price: 310,
  category: "soup",
  kind: "veg",
  count: "330 g",
  image: "png/tomato_soup.jfif"
},
  {
    keyword: "fish_soup",
    name: "Fish soup with vegetables",
    price: 370,
    category: "soup",
    kind: "fish",
    count: "360 g",
    image: "png/fish_soup.jfif"
  },
  {
    keyword: "cream_mushroom_soup",
    name: "Creamy mushroom soup",
    price: 330,
    category: "soup",
    kind: "veg",
    count: "340 g",
    image: "png/mushroom_soup.jpg"
  },

  // ===== MAIN COURSES =====
  {
    keyword: "chicken_rice",
    name: "Grilled chicken with vegetables and rice",
    price: 450,
    category: "main",
    kind: "meat",
    count: "420 g",
    image: "png/Chickenrice.jfif"
  },
  {
    keyword: "salmon",
    name: "Baked salmon with potato puree",
    price: 480,
    category: "main",
    kind: "fish",
    count: "410 g",
    image: "png/fish.jfif"
  },
  {
    keyword: "veg_curry",
    name: "Vegetable curry with chickpeas and rice",
    price: 430,
    category: "main",
    kind: "veg",
    count: "390 g",
    image: "png/Vegetable.jfif"
  },
  {
  keyword: "cod_fillet",
  name: "Cod fillet with vegetables",
  price: 490,
  category: "main",
  kind: "fish",
  count: "430 g",
  image: "png/cod_fillet.jfif"
},

  {
    keyword: "beef_steak",
    name: "Beef steak with sauce",
    price: 520,
    category: "main",
    kind: "meat",
    count: "450 g",
    image: "png/beef_steak.jfif"
  },
  {
    keyword: "tofu_bowl",
    name: "Tofu bowl with vegetables",
    price: 410,
    category: "main",
    kind: "veg",
    count: "400 g",
    image: "png/tofu_bowl.jfif"
  },

  // ===== SALADS & STARTERS =====
  {
    keyword: "salmon_salad",
    name: "Salmon salad",
    price: 390,
    category: "salad",
    kind: "fish",
    count: "220 g",
    image: "png/salmon_salad.jpg"
  },
  {
    keyword: "chicken_caesar",
    name: "Caesar salad with chicken",
    price: 360,
    category: "salad",
    kind: "meat",
    count: "240 g",
    image: "png/caesar.jfif"
  },
  {
    keyword: "avocado_salad",
    name: "Avocado salad",
    price: 300,
    category: "salad",
    kind: "veg",
    count: "210 g",
    image: "png/avocado_salad.jfif"
  },
  {
    keyword: "quinoa_salad",
    name: "Quinoa vegetable salad",
    price: 320,
    category: "salad",
    kind: "veg",
    count: "230 g",
    image: "png/quinoa_salad.jfif"
  },

  // ===== DRINKS =====
  {
    keyword: "morse",
    name: "Homemade cranberry drink",
    price: 120,
    category: "drink",
    kind: "cold",
    count: "300 ml",
    image: "png/Morse.jfif"
  },
  {
    keyword: "lemonade",
    name: "Citrus lemonade with mint",
    price: 150,
    category: "drink",
    kind: "cold",
    count: "300 ml",
    image: "png/lemonade.jfif"
  },
  {
    keyword: "iced_tea",
    name: "Iced tea with lemon",
    price: 130,
    category: "drink",
    kind: "cold",
    count: "300 ml",
    image: "png/iced_tea.jfif"
  },
  {
    keyword: "coffee",
    name: "Americano with milk",
    price: 160,
    category: "drink",
    kind: "hot",
    count: "250 ml",
    image: "png/Coffee.jfif"
  },
  {
    keyword: "hot_chocolate",
    name: "Hot chocolate",
    price: 180,
    category: "drink",
    kind: "hot",
    count: "250 ml",
    image: "png/hot_chocolate.jfif"
  },
  {
  keyword: "green_tea",
  name: "Green tea",
  price: 140,
  category: "drink",
  kind: "hot",
  count: "250 ml",
  image: "png/green_tea.jfif"
},

  // ===== DESSERTS =====
  {
    keyword: "brownie",
    name: "Chocolate brownie",
    price: 230,
    category: "dessert",
    kind: "small",
    count: "90 g",
    image: "png/brownie.jfif"
  },
  {
    keyword: "cheesecake",
    name: "Cheesecake",
    price: 260,
    category: "dessert",
    kind: "medium",
    count: "120 g",
    image: "png/cheesecake.jfif"
  },
  {
    keyword: "fruit_tart",
    name: "Fruit tart",
    price: 280,
    category: "dessert",
    kind: "medium",
    count: "140 g",
    image: "png/fruit_tart.jfif"
  },
  {
    keyword: "big_cake",
    name: "Big chocolate cake",
    price: 520,
    category: "dessert",
    kind: "large",
    count: "350 g",
    image: "png/big_cake.jfif"
  },
  {
  keyword: "tuna_salad",
  name: "Tuna salad",
  price: 370,
  category: "salad",
  kind: "fish",
  count: "230 g",
  image: "png/tuna_salad.jfif"
},
{
  keyword: "grilled_veggies",
  name: "Grilled vegetables starter",
  price: 290,
  category: "salad",
  kind: "veg",
  count: "210 g",
  image: "png/grilled_veggies.jfif"
},
{
  keyword: "ice_cream",
  name: "Vanilla ice cream",
  price: 190,
  category: "dessert",
  kind: "small",
  count: "100 g",
  image: "png/ice_cream.jfif"
},
{
  keyword: "pancakes",
  name: "Pancakes with berries",
  price: 340,
  category: "dessert",
  kind: "large",
  count: "300 g",
  image: "png/pancakes.jfif"
}

];
