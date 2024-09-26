<template>
  <div class="modal" :id="'UpdateBookResource' + bookId" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ newBook.title }}</h5>
        </div>
        <div class="modal-body">
          <form class="form-floating">
            <input type="text" class="form-control" id="floatingInputValue" placeholder="Book Title"
              v-model="newBook.title" required />
            <label for="floatingInputValue">Book Title</label>
          </form>
          <div class="form-floating">
            <input type="text" class="form-control" id="floatingInputValue" placeholder="Book Author"
              v-model="newBook.author" required />
            <label for="floatingInputValue">Book Author</label>
          </div>
          <div class="form-floating">
            <textarea class="form-control" placeholder="Add a description here" id="floatingTextarea"
              v-model="newBook.description" required></textarea>
            <label for="floatingTextarea">Book Description</label>
          </div>
          <div class="form-floating">
            <input type="text" class="form-control" id="floatingInputValue" placeholder="View Username"
              v-model="newBook.view" required/>
            <label for="floatingInputValue">View link</label>
          </div>
          <div class="form-floating">
            <input type="text" class="form-control" id="floatingInputValue" placeholder="Edit Username"
              v-model="newBook.edit" />
            <label for="floatingInputValue">Edit link</label>
          </div>
          <div class="form-floating">
            <input type="number" class="form-control" id="floatingInputValue" placeholder="Book Price"
              v-model.number="newBook.price" required />
            <label for="floatingInputValue">Book Price</label>
          </div>
          <div class="form-floating">
            <input type="date" class="form-control" id="floatingInputValue" placeholder="" v-model="newBook.date"
              required />
            <label for="floatingInputValue">Book Date</label>
          </div>
          <div class="form-floating">
            <input type="number" class="form-control" id="floatingInputValue" placeholder="Book Price"
              v-model.number="newBook.stock" required />
            <label for="floatingInputValue">Book Stock</label>
          </div>
          <div class="form-floating">
            <select class="form-select" id="floatingSelect" v-model="newBook.section_id" aria-label="Section" required>
              <option value="" disabled selected>Select a section</option>
              <option v-for="section in sections" :key="section.genre_id" :value="section.genre_name">
                {{ section.genre_name }}</option>
            </select>
            <label for="floatingSelect">Section</label>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" @click="updateSection">Update</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'UpdateBookResource',
  props: {
    bookId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      newBook: {
        title: '',
        view: '',
        edit: '',
        description: '',
        date: '',
        price: 0,
        stock: 0,
        author: '',
        section_id: ''
      },
      sections: [],
    }
  },
  methods: {
    async updateSection() {
      try {
        const response = await axios.put(
          `http://127.0.0.1:5000/api/books/new/${this.bookId}`,
          {
            name: this.newBook.title,
            view_access_link: this.newBook.view,
            edit_access_link: this.newBook.edit,
            description: this.newBook.description,
            date: this.newBook.date,
            price: this.newBook.price,
            stock: this.newBook.stock,
            author: this.newBook.author,
            section_name: this.newBook.section_id
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 200) {
          console.log(response.data.msg);
          location.reload();
        } else {
          console.log(response.data.msg);
          location.reload();
        }
      } catch (error) {
        console.error("Error fetching sections:", error);
        alert(error);
      }
    },
    fetchSections() {
      axios.get("http://127.0.0.1:5000/api/genres", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      })
        .then((response) => {
          this.sections = response.data;
          console.log(this.sections);
        })
        .catch((error) => {
          console.error("Error fetching sections:", error);
          alert(error);
        });
    },
    fetchBooks() {
            axios.get(`http://127.0.0.1:5000/api/books/new/${this.bookId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            })
            .then((response) => {
                this.newBook.title = response.data.name;
                this.newBook.view = response.data.view_access_link;
                this.newBook.edit = response.data.edit_access_link;
                this.newBook.description = response.data.description;
                this.newBook.date = response.data.date;
                this.newBook.price = response.data.price;
                this.newBook.stock = response.data.stock;
                this.newBook.author = response.data.author;
                this.newBook.section_id = response.data.section_name;
                console.log(this.newSection);
            })
            .catch((error) => {
                console.error("Error fetching sections:", error);
            });
        },
  },
  mounted() {
    this.fetchSections();
    this.fetchBooks();
  },
}
</script>

<style scoped></style>