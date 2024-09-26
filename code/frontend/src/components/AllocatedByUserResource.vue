<template>
  <div>
    <h2>Books Allocated to User</h2>
    <ul>
      <li v-for="book in allocatedBooks" :key="book.id">
        {{ book.title }} - {{ book.author }}
        <button @click="revokeBook(book.id)">Revoke</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AllocatedByUserResource",
  data() {
    return {
      allocatedBooks: [],
    };
  },
  mounted() {
    this.fetchAllocatedBooks();
  },
  methods: {
    fetchAllocatedBooks() {
      axios
        .get("http://127.0.0.1:5000/api/allocated/books", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          this.allocatedBooks = response.data.books;
        })
        .catch((error) => {
          console.error("Error fetching allocated books:", error);
        });
    },
    revokeBook(bookId) {
      axios
        .post(`http://127.0.0.1:5000/api/revoke/book/${bookId}`, null, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
          this.fetchAllocatedBooks();
        })
        .catch((error) => {
          console.error("Error revoking book:", error);
        });
    },
  },
};
</script>