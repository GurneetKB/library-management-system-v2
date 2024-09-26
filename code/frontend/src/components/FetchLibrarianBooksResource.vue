<template>
  <div>
    <ul>
      <li v-for="book in books" :key="book.id">
        {{ book.title }} - {{ book.author }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "FetchLibrarianBooksResource",
  data() {
    return {
      books: [],
    };
  },
  mounted() {
    this.fetchBooks();
  },
  methods: {
    fetchBooks() {
      axios
        .get("http://127.0.0.1:5000/api/librarian/books", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          this.books = response.data.books;
        })
        .catch((error) => {
          console.error("Error fetching books:", error);
        });
    },
  },
};
</script>