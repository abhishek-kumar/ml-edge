<!-- TypeScript -->
<script lang="ts">
    let file: File | null = null;
    let preview: string | ArrayBuffer | null  = '';
  
    function onFileChange(event: Event) {
      const files = (event.target as HTMLInputElement).files;
      if (files && files.length > 0) {
        file = files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
          preview = (e.target! as FileReader).result;
        };
        reader.readAsDataURL(file);
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
</style>

<!-- HTML Code -->
<h1>iRecognize</h1>
  
<div class="center-div">

    <input class="file-input" type="file" accept="image/*" on:change={onFileChange} />

    {#if preview}
    <div class="double-image-preview">
        <img src={preview} alt="Image preview" class="single-image-preview" />
        <img src={preview} alt="Transformed Image" class="single-image-preview" />
    </div>
    {/if}
</div>

<!-- END HTML -->