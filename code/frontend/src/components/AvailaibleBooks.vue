<template>
  <div>
    <LibrarianNavbar />
    <div class="container">
      <div class="all-books mt-4">
        <div class="row">
          <div class="col-sm-8">
            <h3>Available Books</h3>
          </div>
          <div class="col-sm-4 d-flex justify-content-end mb-2">
            <button type="button" class="btn btn-secondary modal-dialog-centered" data-bs-toggle="modal" data-bs-target="#BookResource">
              Add Books
            </button>
            <BookResource />
          </div>
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
                          <div class="">
                            <div class="buttons d-flex justify-content-around">
                              <button type="button" class="btn btn-primary modal-dialog-centered" data-bs-toggle="modal"
                                :data-bs-target="'#UpdateBookResource' + book.id">
                                update
                              </button>
                              <UpdateBookResource :bookId="book.id" />
                              <button type="button" class="btn btn-success" @click="deleteSection(book.id)" >
                                Delete
                              </button>
                            </div>
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
import LibrarianNavbar from "../components/LibrarianNavbar.vue";
import BookResource from "../components/BookResource.vue";
import UpdateBookResource from "../components/UpdateBookResource.vue";
export default {
  name: "AvailableBooks",
  components: {
    LibrarianNavbar,
    BookResource,
    UpdateBookResource
  },
  data() {
    return {
      books: [],
      searchQuery: '', // Data property to hold search query
    };
  },
  methods: {
    async fetchAllBooks() {
      try {
        console.log(process.env.NODE_ENV)
        const response = await axios.get(
          'http://127.0.0.1:5000/api/fetch/librarian/books',
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.books = response.data;
        console.log(this.books);
      } catch (error) {
        console.log(error);
      }
    },
    async deleteSection(id) {
            const confirmDelete = confirm("Are you sure you want to delete this section?")
            if (confirmDelete) {
                try {
                const response = await axios.delete(
                    `http://127.0.0.1:5000/api/books/new/${id}`,
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
                }
            }
        }
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
  created() {
    this.fetchAllBooks();
  },
};
</script>

<style>
.search-section {
  margin-bottom: 20px;
}
</style>
