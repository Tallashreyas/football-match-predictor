const homeTeam = document.getElementById("homeTeam");
const awayTeam = document.getElementById("awayTeam");

const predictBtn = document.getElementById("predictBtn");

const predictionResult = document.getElementById("predictionResult");
const predictionMessage = document.getElementById("predictionMessage");
const probabilities = document.getElementById("probabilities");

const homeStats = document.getElementById("homeStats");
const awayStats = document.getElementById("awayStats");

const API = "http://127.0.0.1:8000";

async function loadTeams(){

    try{

        const response = await fetch(`${API}/teams`);

        const data = await response.json();

        homeTeam.innerHTML = "";
        awayTeam.innerHTML = "";

        data.teams.forEach(team=>{

            homeTeam.innerHTML += `<option value="${team}">${team}</option>`;
            awayTeam.innerHTML += `<option value="${team}">${team}</option>`;

        });

        homeTeam.selectedIndex = 0;
        awayTeam.selectedIndex = 1;

    }

    catch{

        alert("Could not connect to backend.");

    }

}

function progressBar(title,value,color){

    return `

        <div class="probability-item">

            <div class="probability-header">

                <span>${title}</span>

                <span>${value.toFixed(1)}%</span>

            </div>

            <div class="progress">

                <div class="progress-fill"

                    style="width:${value}%;background:${color};">

                </div>

            </div>

        </div>

    `;

}

function predictionIcon(result){

    if(result==="Home Win") return "🏠 Home Win";

    if(result==="Away Win") return "✈️ Away Win";

    return "🤝 Draw";

}

predictBtn.addEventListener("click",async()=>{

    if(homeTeam.value===awayTeam.value){

        alert("Please select different teams.");

        return;

    }

    predictBtn.disabled = true;

    predictBtn.innerHTML = "Predicting...";

    predictionResult.innerHTML = "⚽";

    predictionMessage.innerHTML = "Running Deep Learning Model...";

    probabilities.innerHTML = "";

    try{

        const response = await fetch(`${API}/predict`,{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                home_team:homeTeam.value,

                away_team:awayTeam.value

            })

        });

        const result = await response.json();

        predictionResult.innerHTML = predictionIcon(result.prediction);

        predictionMessage.innerHTML =
            `${homeTeam.value} vs ${awayTeam.value}`;

        probabilities.innerHTML =

            progressBar(
                "Home Win",
                result.probabilities.home,
                "#22C55E"
            ) +

            progressBar(
                "Draw",
                result.probabilities.draw,
                "#F59E0B"
            ) +

            progressBar(
                "Away Win",
                result.probabilities.away,
                "#EF4444"
            );

        homeStats.innerHTML = `

            <h3>${homeTeam.value}</h3>

            <p><strong>Win Rate</strong> : ${(result.home_stats.win_rate*100).toFixed(1)}%</p>

            <p><strong>Goals/Game</strong> : ${result.home_stats.avg_goals.toFixed(2)}</p>

            <p><strong>Shots/Game</strong> : ${result.home_stats.avg_shots.toFixed(2)}</p>

            <p><strong>Goal Difference</strong> : ${result.home_stats.goal_difference.toFixed(2)}</p>

        `;

        awayStats.innerHTML = `

            <h3>${awayTeam.value}</h3>

            <p><strong>Win Rate</strong> : ${(result.away_stats.win_rate*100).toFixed(1)}%</p>

            <p><strong>Goals/Game</strong> : ${result.away_stats.avg_goals.toFixed(2)}</p>

            <p><strong>Shots/Game</strong> : ${result.away_stats.avg_shots.toFixed(2)}</p>

            <p><strong>Goal Difference</strong> : ${result.away_stats.goal_difference.toFixed(2)}</p>

        `;

    }

    catch(err){

        console.log(err);

        alert("Backend connection failed.");

    }

    predictBtn.disabled = false;

    predictBtn.innerHTML = "Predict Match";

});

loadTeams();