<template>
  <div>
    <h2>User Books</h2>
    <ul>
      <li v-for="book in books" :key="book.id">
        {{ book.title }} - {{ book.author }}
        <button @click="returnBook(book.id)">Return</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserBooksResource",
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
        .get("http://127.0.0.1:5000/api/user/books", {
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
    returnBook(bookId) {
      axios
        .post(`http://127.0.0.1:5000/api/return/book/${bookId}`, null, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
          this.fetchBooks();
        })
        .catch((error) => {
          console.error("Error returning book:", error);
        });
    },
  },
};
</script>