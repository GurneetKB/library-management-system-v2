<template>
  <div>
    <h2>Allocate Book Resource</h2>
    <form @submit.prevent="allocateResource">
      <label for="book">Select a book:</label>
      <select id="book" v-model="selectedBook">
        <option v-for="book in books" :key="book.id" :value="book.id">{{ book.title }}</option>
      </select>
      <label for="resource">Select a resource:</label>
      <select id="resource" v-model="selectedResource">
        <option v-for="resource in resources" :key="resource.id" :value="resource.id">{{ resource.name }}</option>
      </select>
      <button type="submit">Allocate</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      books: [
        { id: 1, title: 'Book 1' },
        { id: 2, title: 'Book 2' },
        { id: 3, title: 'Book 3' }
      ],
      resources: [
        { id: 1, name: 'Resource 1' },
        { id: 2, name: 'Resource 2' },
        { id: 3, name: 'Resource 3' }
      ],
      selectedBook: null,
      selectedResource: null
    };
  },
  methods: {
    allocateResource() {
      // Perform the allocation logic here
      console.log('Allocating resource:', this.selectedResource, 'to book:', this.selectedBook);
      // You can make an API call to your backend to perform the allocation
    }
  }
};
</script>