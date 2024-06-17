const main = () => {
  const _elements = {
    checkBtn: document.getElementById("check"),
    checkAgainBtn: document.getElementById("check-again"),
    input: document.getElementById("input"),
    loading: document.getElementById("loading"),
    bsQuery: document.getElementById("bs-query"),
    bsReport: document.getElementById("bs-report"),
  };

  const aiServices = [
    "Checking ChatGPT v5...",
    "Checking Gemini...",
    "Querying blockchains...",
    "Pinging Elon Musk...",
    "Emailing Bill Gates...",
    "Faxing the 1990s...",
  ];

  const placeholders = [
    "The earth is flat.",
    "Butterflies are government drones.",
    "The moon landing was fake.",
    "Light bulbs are sentient.",
    "The sun is a hologram.",
    "The ocean is a simulation.",
    "The sky is a painting.",
    "The grass is a lie.",
    "The trees are listening.",
    "The government is ran by liazard people.",
    "The government is ran by aliens.",
    "Aliens are among us.",
    "Bullshit is everywhere.",
    "Jokes are real.",
    "Flat earthers are right.",
    "Speed of light is not constant.",
    "I am your father.",
    "I am your mother.",
    "The wind is really the trees farting.",
    "Shooting stars are really aliens crashing.",
    "Eating vegetables is bad for you.",
    "Eat too many vegetables and you will turn into a vegetable.",
    "Black holes are really the universe's belly button.",
    "Cats are actually secret agents from an unknown civilization.",
    "The cake is a lie.",
    "We are all living in a simulation.",
  ];
  const placeholder =
    placeholders[Math.floor(Math.random() * placeholders.length)];
  _elements.input.placeholder = `Example: ${placeholder}`;

  const urlParams = new URLSearchParams(window.location.search);
  const initialBsQuery = urlParams.get("bs-query");
  if (initialBsQuery) {
    _elements.input.value = initialBsQuery;
  }

  _elements.checkBtn.addEventListener("click", () => {
    const inputValue = _elements.input.value;
    if (inputValue === "") {
      window.alert("You need to enter something to be checked for bullshit");
      return;
    }
    if (inputValue.length > 1000) {
      window.alert(
        `Due to AI constraints, on our free tier the bullshit query must be less than 1000 characters (current query characters: ${inputValue.length}).`,
      );
      return;
    }
    const url = new URL(window.location.href);
    url.searchParams.set("bs-query", inputValue);
    window.history.pushState({}, "", url);

    _elements.loading.style.display = "block";
    _elements.bsReport.style.display = "none";
    _elements.checkBtn.disabled = true;
    _elements.input.disabled = true;

    const stopAiQuery = startAiQuery();
    setTimeout(() => {
      _elements.loading.style.display = "none";
      _elements.bsReport.style.display = "block";
      _elements.bsQuery.style.display = "none";
      _elements.checkBtn.disabled = false;
      _elements.input.disabled = false;
      stopAiQuery();
    }, 8000);
  });

  _elements.checkAgainBtn.addEventListener("click", () => {
    _elements.bsQuery.style.display = "block";
    _elements.bsReport.style.display = "none";
  });

  const startAiQuery = () => {
    let i = 0;
    _elements.loading.innerText = aiServices[i];

    const interval = setInterval(() => {
      i++;
      _elements.loading.innerText = aiServices[i % aiServices.length];
    }, 1500);
    return () => {
      clearInterval(interval);
    };
  };
};
main();
