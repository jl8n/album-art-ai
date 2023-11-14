<script lang="ts">
    import { onMount } from "svelte";

    let data: string[] | undefined;
    let album = "";
    let artist = "";

    async function fetchData(artist: string, album: string) {
        const params =
            `album=${encodeURIComponent(album)}&` +
            `artist=${encodeURIComponent(artist)}`;
        const url = `http://localhost:5000/?${params}`;
        console.log("URL", url);
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        data = await response.json();
    }

    function handleSubmit() {
        fetchData(artist, album);
    }
</script>

<h1>Album Art AI Trainer</h1>

<form on:submit|preventDefault={handleSubmit}>
    <label for="album">Album:</label>
    <input id="album" bind:value={album} type="text" required />

    <label for="artist">Artist:</label>
    <input id="artist" bind:value={artist} type="text" required />

    <button type="submit">Submit</button>
</form>

{#if data}
    <h2>Choose the best image:</h2>
    <div class="flex">
        {#each data as filename (filename)}
            <button>
                <img
                    src="http://localhost:5000/album-art/{filename}"
                    alt={filename}
                />
            </button>
        {/each}
    </div>
{/if}

<style>
    .flex {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
    }

    .flex > button {
        background: none;
        border: none;
        padding: 0;
        cursor: pointer;
    }

    .flex > button > img {
        width: 400px;
    }
</style>
