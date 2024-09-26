<template>
  <div>
    <UserNavbar />
    <div class="container">
      <div class="all-books mt-4">
        <div class="row">
          <h3>All Books</h3>
        </div>

        <!-- Search box -->
        <div class="search-section">
          <input type="text" v-model="searchQuery" placeholder="Search books..." class="form-control">
        </div>
        <div class="row">
          <div class="col-md-12">
            <div class="card">
              <div class="card-body">
                <div v-if="filteredBooks.length > 0">
                  <table class="table table-bordered">
                    <thead>
                      <tr>
                        <th>Book Name</th>
                        <th>Author</th>
                        <th>Section</th>
                        <th>Availability</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="book in filteredBooks" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.author }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>{{ book.stock }}</td>
                        <td>
                          <div class="button">
                            <button v-if="book.request_status < 0" type="button"
                              class="btn btn-request_again" @click="handleRequest(book.id)">
                              Request
                            </button>
                            <button v-else-if="book.request_status === 3 || book.request_status === 2" type="button" @click="handleRequest(book.id)" class="btn btn-completed">
                              Request Again
                            </button>
                            <button v-else-if="book.request_status === 1" type="button" class="btn btn-completed">
                              Already Allocated ({{ book.request_status }})
                            </button>
                            <button v-else-if="book.request_status === 0" type="button" class="btn btn-warning">
                              Already Request
                            </button>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div v-else>
                  <p>No books available right now.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UserNavbar from "../components/UserNavbar.vue";
export default {
  name: "AllBooks",
  components: {
    UserNavbar,
  },
  data() {
    return {
      books: [],
      searchQuery: '',
    };
  },
  created() {
    this.fetchBooks();
  },
  methods: {
    fetchBooks() {
      axios
        .get("http://127.0.0.1:5000/api/books", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          this.books = response.data;
          console.log(this.books);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleRequest(bookId) {
      console.log(bookId);
      const requestData = {
        id: bookId,
      };
      axios.post("http://127.0.0.1:5000/api/books/allocate", requestData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      })
        .then((response) => {
          console.log(response.data);
          console.log("Request sent");
          this.fetchBooks();
        })
        .catch((error) => {
          alert(error.response.data.error)
          console.log(error);
        });
    },
  },
  computed: {
    filteredBooks() {
      return this.books.filter(book =>
        book.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.author.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.section_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.stock.toString().includes(this.searchQuery)
      );
    }
  },
};
</script>

<style>
.search-section {
  margin-bottom: 20px;
}
</style>