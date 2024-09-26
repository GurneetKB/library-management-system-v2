<template>
  <div>
    <LibrarianNavbar />
    <div class="container">
      <div class="all-books mt-4">
        <div class="row">
          <h3>Allocated Books</h3>
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
                        <th>User Name</th>
                        <th>Section</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="book in filteredBooks" :key="book.book_id">
                        <td>{{ book.book_name }}</td>
                        <td>{{ book.user_name }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>
                          <button class="btn btn-danger mw-100" @click="
                            revokeAccess(book.allocation_id, book.book_id, book.user_id)
                            ">
                            Revoke
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div v-else>
                  <p>No allocated books right now.</p>
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
import LibrarianNavbar from "../components/LibrarianNavbar.vue";
import axios from "axios";
export default {
  name: "AllocatedBooks",
  components: {
    LibrarianNavbar,
  },
  data() {
    return {
      allocatedBooks: [],
      searchQuery: '',
    };
  },
  created() {
    this.getAllocatedBooks();
  },
  computed: {
    filteredBooks() {
      return this.allocatedBooks.filter(book =>
        book.book_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.authors.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.section_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.status.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async getAllocatedBooks() {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/librarian/allocated_books",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (!response.ok) {
          throw new Error("Failed to fetch allocated books");
        }
        const data = await response.json();
        this.allocatedBooks = data;
        console.log(data);
      } catch (error) {
        console.error("Error:", error.message);
      }
    },
    async revokeAccess(allocation_id, book_id, user_id) {
      // console.log("Revoke access for allocation_id:", allocation_id, "book_id:", book_id);
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/revoke/book",
          {
            allocation_id: allocation_id,
            book_id: book_id,
            user_id: user_id,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          console.log("Book returned successfully");
          this.getAllocatedBooks();
        } else {
          console.error("Failed to return the book");
        }
      } catch (error) {
        console.error("Error returning the book:", error);
      }
    },
  },
};
</script>

<style>
.search-section {
  margin-bottom: 20px;
}
</style>