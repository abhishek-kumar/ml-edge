<script>
    let review = '';
    let result = '';

    function submitReview() {
        fetch('http://localhost:8080/api/review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ review })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                result = data.result; // Assume the sentiment analysis result is in data.result
            } else {
                alert('Error submitting review');
            }
        });
    }
</script>


<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; font-family: Arial, sans-serif;">
    <h1 style="color: #333; margin-bottom: 20px;">Sentiment Analysis</h1>
    <textarea
        bind:value={review}
        style="width: 500px; height: 200px; padding: 10px; font-size: 16px; border-radius: 4px; border: 1px solid #ccc;"
    ></textarea>
    <button
        on:click={submitReview}
        style="margin-top: 10px; padding: 10px 20px; font-size: 16px; color: white; background-color: #007BFF; border: none; border-radius: 4px; cursor: pointer;"
    >
        Submit Review
    </button>
    {#if result}
        <h2 style="margin-top: 20px;">Result: {result}</h2>
    {/if}
</div>
