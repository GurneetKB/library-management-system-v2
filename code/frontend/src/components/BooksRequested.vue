<template>
  <div>
    <LibrarianNavbar />
    <div class="container">
      <div class="all-books mt-4">
        <div class="row">
          <h3>Available Requested</h3>
        </div>
        <div class="search-section">
          <input type="text" v-model="searchQuery" placeholder="Search books..." class="form-control">
        </div>
        <div class="row">
          <div class="col-md-12">
            <div class="card">
              <div class="card-body">
                <div v-if="filteredRequests.length > 0">
                  <table class="table table-bordered">
                    <thead>
                      <tr>
                        <th>Book Name</th>
                        <th>Requested By</th>
                        <th>Give</th>
                        <th>Revoke</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="book in filteredRequests" :key="book.id">
                        <td>{{ book.book_name }}</td>
                        <td>{{ book.username }}</td>
                        <td>
                          <button class="btn btn-success" @click="
                            grantBookRequest(
                              book.id
                            )
                            ">
                            Grant
                          </button>
                        </td>
                        <td>
                          <button class="btn btn-danger" @click="revokeAccess(book.id)">
                            Reject
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div v-else>
                  <p>No requested books right now.</p>
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
export default {
  name: "BooksRequested",
  components: {
    LibrarianNavbar,
  },
  data() {
    return {
      requestedBooks: [],
      searchQuery: '',
    };
  },
  mounted() {
    this.fetchRequestedBooks();
  },
  methods: {
    async fetchRequestedBooks() {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/books/requested",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const data = await response.json();
        if (response.ok) {
          this.requestedBooks = data;
          console.log("Requested books: ", data);
        } else {
          console.error("Failed to fetch requested books: ", data.error);
        }
      } catch (error) {
        console.error("Error fetching requested books: ", error);
      }
    },
    async grantBookRequest(bookId) {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/books/allocate",
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify({
              req_id: bookId
            }),
          }
        );
        const data = await response.json();
        if (response.ok) {
          console.log("Book request granted successfully: ", data.message);
          this.fetchRequestedBooks();
        } else {
          console.error("Failed to grant book request: ", data.error);
        }
      } catch (error) {
        console.error("Error granting book request: ", error);
      }
    },
    async revokeAccess(allocationId) {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/delete/request",
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify({
              req_id: allocationId,
            }),
          }
        );


        if (!response.ok) {
          throw new Error("Failed to revoke access");
        }
        else {
          this.fetchRequestedBooks();
        }

        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error("Error revoking access:", error);
      }
    },
  },
  computed: {
    filteredRequests() {
      return this.requestedBooks.filter(book =>
        book.book_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.authors.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.section_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.status.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
};
</script>

<style scoped>
.btn {
  display: flex;
  justify-content: center;
  background-color: coral;
  color: white;
  border: none;
  margin-left: 10px;
  margin-top: 5px;
  margin-bottom: 5px;
  padding: 5px 10px;
}

.btn:hover {
  background-color: #ff4500;
}
</style>
