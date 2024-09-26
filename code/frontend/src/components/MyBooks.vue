<template>
  <div>
    <UserNavbar />
    <div class="container">
      <div class="row mt-4">
        <div class="row">
          <h3>Current</h3>
        </div>
        <div class="search-section">
          <input type="text" v-model="searchQuery1" placeholder="Search books..." class="form-control">
        </div>
        <div class="row">
          <div v-if="filteredmyBooks.length > 0">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Book Name</th>
                  <th>Author</th>
                  <th>Section</th>
                  <th>Function</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="book in filteredmyBooks" :key="book.id">
                  <td>{{ book.book_title }}</td>
                  <td>{{ book.author }}</td>
                  <td>{{ book.section }}</td>
                  <td class="ano d-flex justify-content-around">
                    <button type="button" class="btn" style="background-color: rgb(12, 183, 0);" @click="
                      readBook(book.content)
                      ">
                      Read
                    </button>
                    <button type="button" class="btn btn-warning" @click="
                      returnBook(
                        book.id
                      )
                      ">
                      Return
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No books available.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="row mt-4">
        <div class="row">
          <h3>Completed</h3>
        </div>
        <div class="search-section">
          <input type="text" v-model="searchQuery2" placeholder="Search books..." class="form-control">
        </div>
        <div class="row">
          <div v-if="filteredreturnedBooks.length > 0">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Book Name</th>
                  <th>Author</th>
                  <th>Section</th>
                  <th>Function</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="book in filteredreturnedBooks" :key="book.id">
                  <td>{{ book.book_title }}</td>
                  <td>{{ book.author }}</td>
                  <td>{{ book.section }}</td>
                  <td v-if="book.rate">
                    <Rating v-model="book.rate" readonly />
                  </td>
                  <td v-else>
                    <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                      :data-bs-target="'#staticBackdrop' + book.book_id">
                      Feedback
                    </button>
                    <FeedbackModal :bookId="book.book_id" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No books available.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UserNavbar from "../components/UserNavbar.vue";
import FeedbackModal from "./FeedbackModal.vue";
import Rating from 'primevue/rating';
export default {
  name: "MyBooks",
  components: {
    UserNavbar,
    FeedbackModal,
    Rating
  },
  data() {
    return {
      myBooks: [],
      returnedBooks: [],
      searchQuery1: '',
      searchQuery2: '',
    };
  },
  methods: {
    async fetchMyBooks() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/fetch_my_books",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          console.log("My Books:", response.data);
          this.myBooks = response.data.myBooks;
          this.returnedBooks = response.data.returnedBooks;
          console.log(this.myBooks, this.returnedBooks);
        } else {
          console.error("Failed to fetch my books");
        }
      } catch (error) {
        console.error("Error fetching my books:", error);
      }
    },
    async returnBook(book_id) {
      try {
        const response = await axios.put(
          "http://127.0.0.1:5000/api/return/book",
          {
            registration_id: book_id
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          console.log("Book returned successfully");
          this.fetchMyBooks();
        } else {
          console.error("Failed to return the book");
        }
      } catch (error) {
        console.error("Error returning the book:", error);
      }
    },
    async readBook(content) {
      console.log(content);
      const linkUrl = content;
      window.open(linkUrl, "_blank");
    }
  },
  computed: {
    filteredmyBooks() {
      return this.myBooks.filter(book =>
        book.book_title.toLowerCase().includes(this.searchQuery1.toLowerCase()) ||
        book.author.toLowerCase().includes(this.searchQuery1.toLowerCase()) ||
        book.section.toString().includes(this.searchQuery1)
      );
    },
    filteredreturnedBooks() {
      return this.returnedBooks.filter(book =>
        book.book_title.toLowerCase().includes(this.searchQuery2.toLowerCase()) ||
        book.author.toLowerCase().includes(this.searchQuery2.toLowerCase()) ||
        book.section.toString().includes(this.searchQuery2)
      );
    }
  },
  mounted() {
    this.fetchMyBooks();
  },
};
</script>

<style>
</style>