document.querySelectorAll('.custom-select .option').forEach(function(option) {
    option.addEventListener('click', function() {
        let select = option.closest('.custom-select');
        let selectedValue = option.getAttribute('data-value');
        let currentSelectedOption = select.querySelector('.option[selected]');

        if (currentSelectedOption === option) {
            currentSelectedOption.removeAttribute('selected');
            select.querySelector('.option:first-child').textContent = `Selecione seu ${select.id}`; 
            select.querySelector('.option:first-child').removeAttribute('data-value');
            select.querySelector('.option:first-child').classList.remove('selected');
        } 
        else {
            if (currentSelectedOption) {
                currentSelectedOption.removeAttribute('selected');
                currentSelectedOption.classList.remove('selected');
            }
            option.setAttribute('selected', 'true');
            option.classList.add('selected');
            select.querySelector('.option:first-child').textContent = option.textContent;
            select.querySelector('.option:first-child').setAttribute('data-value', selectedValue);
        }
    });
});

document.getElementById('team-form').addEventListener('submit', function(event) {
    event.preventDefault();
    let selectedTeam = [];
    document.querySelectorAll('.custom-select').forEach(function(select) {
        let selectedOption = select.querySelector('.option[selected]');
        if (selectedOption.textContent !== null && selectedOption.textContent !== '') {
            selectedTeam.push(selectedOption.textContent.trim());
        }
    });
    if (Object.keys(selectedTeam).length > 0) {
        console.log('Time Selecionado:', selectedTeam);
        fetch('/submit-form', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  // This tells Flask that the body is in JSON format
            },
            body: JSON.stringify(selectedTeam),  // Sending the selected team as JSON
        });
    }
});

document.getElementById('submit-button').addEventListener('click', async function() {
    const teamsResponse = await fetch('/get_teams');
    const teams = await teamsResponse.json();

    const charactersResponse = await fetch('/get_characters');
    const characters = await charactersResponse.json();

    const teamDisplay = document.getElementById('team-display');
    const recommendedTitle = document.getElementById('recommended-teams-title');
    
    teamDisplay.innerHTML = '';
    recommendedTitle.classList.add('show');

    teams.forEach((team, index) => {
        const teamDiv = document.createElement('div');
        teamDiv.classList.add('team');

        const teamTitle = document.createElement('div');
        teamTitle.classList.add('team-title');
        teamTitle.textContent = `Time ${index + 1}`;
        teamDiv.appendChild(teamTitle);

        const teamCharactersDiv = document.createElement('div');
        teamCharactersDiv.classList.add('team-characters');

        team.forEach((characterName, idx) => {
            const characterDiv = document.createElement('div');
            characterDiv.classList.add('character');

            const img = document.createElement('img');
            img.src = characters[characterName]; 
            img.alt = characterName;

            const name = document.createElement('div');
            name.classList.add('character-name');
            name.textContent = characterName;

            characterDiv.appendChild(img);
            characterDiv.appendChild(name);
            
            teamCharactersDiv.appendChild(characterDiv);
        });

        teamDiv.appendChild(teamCharactersDiv);
        teamDisplay.appendChild(teamDiv);
    });

    // Mostrar os times com animação
    setTimeout(() => {
        teamDisplay.classList.add('show');
    }, 100);
   
    setTimeout(function() {
        recommendedTitle.scrollIntoView({
            behavior: 'smooth'
        });
    }, 100);
});
