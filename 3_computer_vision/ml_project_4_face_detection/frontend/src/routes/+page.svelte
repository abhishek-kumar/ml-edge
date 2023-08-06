<!-- TypeScript -->
<script lang="ts">

    let file: File | null = null;
    let preview: string | ArrayBuffer | null  = null;
    let transformedImage: string | ArrayBuffer | null = null;
    let isLoading: boolean = false;

    function delay(ms: number) {
        return new Promise( resolve => setTimeout(resolve, ms) );
    }

    async function onFileChange(event: Event) {
      const files = (event.target as HTMLInputElement).files;
      if (files && files.length > 0) {
        file = files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
          preview = (e.target! as FileReader).result;
        };
        reader.readAsDataURL(file);

        let formData = new FormData();

        formData.append("file", file);

        isLoading = true;

        await delay(2000);

        const response = await fetch("http://localhost:8000/detect_faces", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            console.error("There was an error", response);
        } else {
            const result = await response.json();
            transformedImage = `data:${file.type};base64,${result.image}`;
        }

        isLoading = false;
      }
    }
  </script>

<!-- END TypeScript -->

<style>
    .single-image-preview {
        max-width: 500px;
        max-height: 500px;
    }
    .double-image-preview {
        display: flex;
        justify-content: space-between;
        width: 100%;
        max-width: 1000px;
    }
    h1 {
        text-align: center;
        font-size: 3em;
        color: #333;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    .center-div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 50vh;
    }
    .file-input {
        margin-bottom: 20px;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #010101;
        border-radius: 5px;
        background-color: #26ef30;
        cursor: pointer;
    }

    /* Make the isLoading dots look nice */
    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    .loading-dots {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 60px;
    }

    .loading-dots div {
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background: #333;
        animation: loading 0.8s infinite;
    }

    .loading-dots div:nth-child(2) {
        animation-delay: 0.2s;
    }

    .loading-dots div:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes loading {
        0% {
            transform: scale(0);
        }
        50% {
            transform: scale(1);
        }
        100% {
            transform: scale(0);
        }
    }

</style>

<!-- HTML Code -->
<h1>iRecognize</h1>

<div class="center-div">

    <input class="file-input" type="file" accept="image/*" on:change={onFileChange} />

    <div class="double-image-preview">
            {#if preview}
                <img src={preview} alt="Elf 1" class="single-image-preview" />
            {/if}
            {#if isLoading}
                <div class="loading-container">
                    <div class="loading-dots">
                        <div></div>
                        <div></div>
                        <div></div>
                    </div>
                </div>
            {:else if transformedImage}
                <img src={transformedImage} alt="Elf 2" class="single-image-preview" />
            {/if}
    </div>
</div>

<!-- END HTML -->
