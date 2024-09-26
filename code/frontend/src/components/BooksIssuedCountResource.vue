<template>
  <div>
    <p>Books Issued: {{ booksIssuedCount }}</p>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "BooksIssuedCountResource",
  data() {
    return {
      booksIssuedCount: 0,
    };
  },
  mounted() {
    this.fetchBooksIssuedCount();
  },
  methods: {
    fetchBooksIssuedCount() {
      axios
        .get("http://127.0.0.1:5000/api/books/issued/count", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          this.booksIssuedCount = response.data.count;
        })
        .catch((error) => {
          console.error("Error fetching books issued count:", error);
        });
    },
  },
};
</script>