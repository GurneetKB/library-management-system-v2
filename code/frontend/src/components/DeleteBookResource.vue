<template>
  <div>
    <button @click="deleteBook">Delete Book</button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "DeleteBookResource",
  props: {
    bookId: {
      type: Number,
      required: true,
    },
  },
  methods: {
    deleteBook() {
      axios
        .delete(`http://127.0.0.1:5000/api/delete/book/${this.bookId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
        })
        .catch((error) => {
          console.error("Error deleting book:", error);
        });
    },
  },
};
</script>