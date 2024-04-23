function completionCheck() {
    fetch("/getProccessStatus")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.status === "complete") 
        {
            window.location.href = "/output";
        }
      })
      .catch((error) => {
        console.log("Error fetching File Name :", error);
      });
  }
  var intervalId = setInterval(completionCheck, 100);