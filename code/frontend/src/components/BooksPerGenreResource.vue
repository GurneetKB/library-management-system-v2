<template>
  <div>
    <h2>Books per Genre</h2>
    <div v-for="genre in genres" :key="genre.name">
      <h3>{{ genre.name }}</h3>
      <ul>
        <li v-for="book in genre.books" :key="book.id">
          {{ book.title }} - {{ book.author }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "BooksPerGenreResource",
  data() {
    return {
      genres: [],
    };
  },
  mounted() {
    this.fetchBooksPerGenre();
  },
  methods: {
    fetchBooksPerGenre() {
      axios
        .get("http://127.0.0.1:5000/api/books/per/genre", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          this.genres = response.data.genres;
        })
        .catch((error) => {
          console.error("Error fetching books per genre:", error);
        });
    },
  },
};
</script>