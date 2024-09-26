<template>
    <div class="modal fade" :id="'staticBackdrop' + bookId" data-bs-backdrop="static" data-bs-keyboard="false"
        tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="staticBackdropLabel">
                        Please leave a feedback
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <Rating v-model="value" />
                        </div>
                        <div class="mb-3">
                            <label for="message-text" class="col-form-label">Comments:</label>
                            <textarea class="form-control" id="message-text" v-model="comments" required></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn" style="background-color: rgb(213, 0, 0);" data-bs-dismiss="modal">
                        Close
                    </button>
                    <button type="button" class="btn" style="background-color: rgb(12, 183, 0);"
                        @click="handleSubmitFeedback()">
                        Submit
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

import Rating from 'primevue/rating';

export default {
    name: 'FeedbackModal',
    props: {
        bookId: {
            type: String,
            required: true
        }
    },
    components: {
        Rating
    },
    data() {
        return {
            value: null,
            comments: ""
        }
    },
    methods: {
        async handleSubmitFeedback() {
            try {
                const response = await axios.post(
                    "http://127.0.0.1:5000/api/add/feedback",
                    {
                        id: this.bookId,
                        rate: this.value,
                        comments: this.comments
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                        },
                    }
                );
                if (response.status === 200) {
                    console.log("My Books:", response.data);
                    location.reload();
                } else {
                    console.error("Failed to fetch my books");
                }
            } catch (error) {
                console.error("Error fetching my books:", error);
            }
        },
    },
}
</script>

<style scoped></style>