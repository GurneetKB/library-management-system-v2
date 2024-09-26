<template>
  <div>
    <button @click="revokeBook">Revoke Book</button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "RevokeBookResource",
  props: {
    bookId: {
      type: Number,
      required: true,
    },
  },
  methods: {
    revokeBook() {
      axios
        .post(`http://127.0.0.1:5000/api/revoke/book/${this.bookId}`, null, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          alert(response.data.message);
        })
        .catch((error) => {
          console.error("Error revoking book:", error);
        });
    },
  },
};
</script>