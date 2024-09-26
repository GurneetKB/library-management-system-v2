<template>
  <div>
    <LibrarianNavbar />
    <div class="container">
      <div class="all-sections mt-4">
        <div class="row">
          <div class="col-sm-8">
            <h3>Available Sections</h3>
          </div>
          <div class="col-sm-4 d-flex justify-content-end mb-2">
            <button type="button" class="btn btn-secondary modal-dialog-centered" data-bs-toggle="modal"
              data-bs-target="#SectionResource">
              Add Section
            </button>
            <AddSectionModal />
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
                <div v-if="filteredSections.length > 0">
                  <table class="table table-bordered">
                    <thead>
                      <tr>
                        <th>Section Name</th>
                        <th>Date created</th>
                        <th>Description</th>
                        <th>Functions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="section in filteredSections" :key="section.genre_name">
                        <td>{{ section.genre_name }}</td>
                        <td>{{ section.genre_created_date }}</td>
                        <td>{{ section.genre_descp }}</td>
                        <td>
                          <div class="">
                            <div class="buttons d-flex justify-content-around">
                              <button type="button" class="btn btn-primary modal-dialog-centered" data-bs-toggle="modal"
                                :data-bs-target="'#addBookModal' + section.genre_name">
                                Add Books
                              </button>
                              <AddBookModal :sectionId="section.genre_name" />
                              <button type="button" class="btn btn-success align-self-start" data-bs-toggle="modal"
                                :data-bs-target="'#viewSectionModal' + section.genre_id">
                                View Section
                              </button>
                              <ViewSectionModal :sectionId="section.genre_id" />
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
import LibrarianNavbar from "../components/LibrarianNavbar.vue";
import AddBookModal from "../components/AddBookModal.vue";
import ViewSectionModal from "../components/ViewSectionModal.vue";
import AddSectionModal from "../components/AddSectionModal.vue";
import axios from "axios";
import DOMPurify from "dompurify";
export default {
  name: "AvailaibleSection",
  components: {
    LibrarianNavbar,
    AddBookModal,
    ViewSectionModal,
    AddSectionModal
  },
  data() {
    return {
      newSection: {
        title: "",
        date: "",
        description: "",
      },
      sections: [],
      newBook: {
        title: "",
        authorName: "",
        content: "",
        section: "",
      },
      searchQuery: "", // Data property to hold search query
    };
  },
  mounted() {
    this.fetchSections();
  },
  computed: {
    // Filter sections based on search query
    filteredSections() {
      if (this.searchQuery === "") {
        return this.sections
      }
      else {
        return this.sections.filter(section =>
          section.genre_name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
    }
  },
  methods: {
    saveSection() {
      this.newSection.title = DOMPurify.sanitize(this.newSection.title);
      this.newSection.date = DOMPurify.sanitize(this.newSection.date);
      this.newSection.description = DOMPurify.sanitize(this.newSection.description);
      axios.post("http://127.0.0.1:5000/api/genres/new", this.newSection, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      })
        .then((response) => {
          console.log("Section added successfully.", response.data);
          location.reload();
          alert(response.data.msg);
        })
        .catch((error) => {
          console.error("Error adding section:", error);
        });
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
        });
    },
    addBook() {
      console.log(this.newBook);
      this.newBook.title = DOMPurify.sanitize(this.newBook.title);
      this.newBook.authorName = DOMPurify.sanitize(this.newBook.authorName);
      this.newBook.content = DOMPurify.sanitize(this.newBook.content);
      this.newBook.section = DOMPurify.sanitize(this.newBook.section);
      axios.post("http://127.0.0.1:5000/api/add/book", this.newBook, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      })
        .then((response) => {
          alert(response.data.message);
          this.newBook = {
            title: "",
            authorName: "",
            content: "",
            section: "Please select the section to add the book to.",
          };
        })
        .catch((error) => {
          console.error("Error adding book:", error);
        });
    },
    setSection(sectionName) {
      this.newBook.section = sectionName;
    },
  },
};
</script>

<style>
.search-section {
  margin-bottom: 20px;
}
</style>