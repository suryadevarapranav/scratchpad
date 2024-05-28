// fetch is a function used for making HTTP requets to fetch resources. (JSON style data, images and files).
// Simplifies asynchronous data fetching in JavaScript and used for interacting with APIs to retrieve and send data asynchronously over the web.
// fetch (url, {options}). One common property is the method, GET is the default and we have POST, PUT, DELETE.

// fetch function is based on promise, it either resolved or rejected.

// pikachu url

// fetch("https://pokeapi.co/api/v2/pokemon/pikachu")
//     .then(response => {

//         if(!response.ok) {
//             throw new Error("Could not fetch the Pokemon.");
//         }
        
//         return response.json();
//     }) // .then(response => console.log(response)) // also promise based.
//     .then(data => console.log(data.w))
//     .catch(error => console.error(error))

// If we use an async function, we can use an await in it.

// fetchData();

// async function fetchData(){

//     try{
//         const response = await fetch("https://pokeapi.co/api/v2/pokemon/typhlosion");

//         if(!response.ok) {
//             throw new Error("Could not fetch the Pokemon.");
//         }
                    
//         const data = await response.json();
//         console.log(data)

//     } catch(error) {
//         console.error(error);
//     }
// }

// fetchData();

async function fetchData(){

    try{

        const pokemonName = document.getElementById("pokemonName").value.toLowerCase();


        const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemonName}`);

        if(!response.ok) {
            throw new Error("Could not fetch the Pokemon.");
        }
                    
        const data = await response.json();

        // console.log(data);

        const pokemonSprite = data.sprites.front_default;

        const imgElement = document.getElementById("pokemonSprite");

        imgElement.src = pokemonSprite;
        imgElement.style.display = "block";

    } catch(error) {
        console.error(error);
    }
}