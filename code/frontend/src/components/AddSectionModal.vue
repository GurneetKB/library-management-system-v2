<template>
  <div class="modal fade" id="SectionResource" tabindex="-1" aria-labelledby="exampleModalLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
              <div class="modal-content">
                <div class="modal-header">
                  <h1 class="modal-name fs-5" id="exampleModalLabel">
                    Add a new section
                  </h1>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <form class="form-floating">
                    <input type="email" class="form-control" id="floatingInputValue" placeholder="name@example.com"
                      v-model="newSection.name" required />
                    <label for="floatingInputValue">Section Title</label>
                  </form>
                  <div class="form-floating">
                    <input type="date" class="form-control" id="floatingInputValue" placeholder=""
                      v-model="newSection.date" required />
                    <label for="floatingInputValue">Date</label>
                  </div>
                  <div class="form-floating">
                    <textarea class="form-control" placeholder="Add a description here" id="floatingTextarea"
                      v-model="newSection.description" required></textarea>
                    <label for="floatingTextarea">Description</label>
                  </div>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                    Close
                  </button>
                  <button type="button" class="btn btn-primary" @click="saveSection">
                    Save changes
                  </button>
                </div>
              </div>
            </div>
          </div>
</template>

<script>
import axios from "axios";
import DOMPurify from "dompurify";
export default {
  name: 'AddSectionModal',
  data() {
      return {
        newSection: {
        name: "",
        date: "",
        description: "",
      },
      }
  },
  methods: {
    saveSection() {
      this.newSection.name = DOMPurify.sanitize(this.newSection.name);
      this.newSection.date = DOMPurify.sanitize(this.newSection.date);
      this.newSection.description = DOMPurify.sanitize(this.newSection.description);
      axios.post("http://127.0.0.1:5000/api/genres/new", this.newSection, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      })
        .then((response) => {
          console.log("Section added successfully.", response.data);
          // reload the page
          location.reload();
          alert(response.data.msg);
        })
        .catch((error) => {
          console.error("Error adding section:", error);
          alert(error);
        });
    },
  },
}
</script>

<style scoped></style>