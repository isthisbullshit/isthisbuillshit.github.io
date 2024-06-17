const main = () => {
  const _elements = {
    checkBtn: document.getElementById("check"),
    input: document.getElementById("input"),
    loading: document.getElementById("loading"),
    bsReport: document.getElementById("bs-report"),
  };

  const services = [
    "Checking ChatGPT v5...",
    "Checking Gemini...",
    "Querying blockchains...",
    "Pinging Elon Musk...",
    "Emailing Bill Gates...",
    "Texting your mom...",
  ];

  _elements.checkBtn.addEventListener("click", () => {
    const inputValue = _elements.input.value;
    if (inputValue === "") {
      window.alert("You need to enter something to be checked for bullshit");
      return;
    }

    _elements.loading.style.display = "block";
    _elements.checkBtn.disabled = true;
    _elements.bsReport.style.display = "none";

    const stopAiQuery = startAiQuery();
    setTimeout(() => {
      _elements.loading.style.display = "none";
      _elements.checkBtn.disabled = false;
      _elements.bsReport.style.display = "block";
      stopAiQuery();
    }, 8000);
  });

  const startAiQuery = () => {
    let i = 0;
    _elements.loading.innerText = services[i];

    const interval = setInterval(() => {
      i++;
      _elements.loading.innerText = services[i % services.length];
    }, 1500);
    return () => {
      clearInterval(interval);
    };
  };
};
main();
