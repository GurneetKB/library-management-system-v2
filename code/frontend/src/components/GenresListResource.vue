<template>
  <div>
    <h2>Genres List</h2>
    <ul>
      <li v-for="genre in genres" :key="genre.id">
        {{ genre.name }}
        <button @click="deleteGenre(genre.id)">Delete</button>
      </li>
    </ul>
    <div>
      <label for="name">Name:</label>
      <input type="text" id="name" v-model="newGenre.name">
      <button @click="createGenre">Create</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "GenresListResource",
  data() {
    return {
      genres: [],
      newGenre: {
        name: "",
      },
    };
  },
  mounted() {
    this.fetchGenres();
  },
  methods: {
    fetchGenres() {
      axios
        .get("http://127.0.0.1:5000/api/genres", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          this.genres = response.data.genres;
        })
        .catch((error) => {
          console.error("Error fetching genres:", error);
        });
    },
    createGenre() {
      axios
        .post("http://127.0.0.1:5000/api/genres", this.newGenre, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
          this.newGenre.name = "";
          this.fetchGenres();
        })
        .catch((error) => {
          console.error("Error creating genre:", error);
        });
    },
    deleteGenre(genreId) {
      axios
        .delete(`http://127.0.0.1:5000/api/genres/${genreId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
          this.fetchGenres();
        })
        .catch((error) => {
          console.error("Error deleting genre:", error);
        });
    },
  },
};
</script>