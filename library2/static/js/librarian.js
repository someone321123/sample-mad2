const AddSection = {
    data() {
        return {
            sectionName: '',
            sectionDescription: '',
            date: new Date().toLocaleDateString()
        };
    },
    template: `
    <div class="creationform">
        <div class="container">
            <h3 align="center">Add New Section</h3> <br>
            <form method="POST" action="/add-section">
                <div class="mb-3">
                    <label for="SectionName" class="form-label">Section Name</label>
                    <input type="text" class="form-control" id="SectionName" name="SectionName">
                </div>
                <div class="mb-3">
                    <label for="SecDesc" class="form-label">Section Description</label>
                    <textarea type="textarea" class="form-control" id="SecDesc" name="SecDesc"></textarea>
                </div>
                <div class="mb-3">
                    <h5>Date Created : {{date}}</h5>
                </div><br>
                <div class="row" align="center">
                    <div class="col">
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </div>
                    <div class="col">
                        <router-link to="/" class="btn btn-danger">Close</router-link>
                    </div>
                </div>
          </form>
        </div>
    </div>
    `
};


const EditSection={
    template:`
    <div class="creationform">
        <div class="container">
            <h3 align="center">Edit Section</h3> <br>
            <form method="POST" action="/edit-section">
                <div class="mb-3">
                    <input type="number" id="SectionID" name="SectionID" :value="$route.query.section_id" hidden>
                    <label for="SectionName" class="form-label">Section Name</label>
                    <input type="text" class="form-control" id="SectionName" name="SectionName" :value="$route.query.SectionName">
                </div>
                <div class="mb-3">
                    <label for="SecDesc" class="form-label">Section Description</label>
                    <textarea type="textarea" class="form-control" id="SecDesc" name="SecDesc">{{$route.query.SecDesc}}</textarea>
                </div>
                <div class="row" align="center">
                    <div class="col">
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </div>
                    <div class="col">
                        <router-link to="/" class="btn btn-danger">Close</router-link>
                    </div>
                </div>
          </form>
        </div>
    </div>
    `
}




const AddBook = {
    template:`
    <div class="creationform2">
    <div class="container">
        <h3 align="center">Add New Book</h3> <br>
        <form method="POST" action="/add-book">
            <div class="mb-3">
                <label for="BookName" class="form-label">Book Name</label>
                <input type="text" class="form-control" id="BookName" name="bookName">
            </div>
            <div class="mb-3">
                <label for="AuthorName" class="form-label">Author Name</label>
                <input type="text" class="form-control" id="AuthorName" name="authorName"></input>
            </div>
            <input type="hidden" name="sectionName" :value="$route.query.SectionName">
            <div class="mb-3">
                <h5>Book Section : {{ $route.query.SectionName }}</h5>
            </div><br>
            <div class="row" align="center">
                <div class="col">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </div>
                <div class="col">
                    <router-link to="/" class="btn btn-danger">Close</router-link>
                </div>
            </div>
      </form>
    </div>
</div>
    `
};




const routes = [
    { path: '/add-book', component: AddBook },
    { path: '/add-section', component: AddSection },
    { path: '/edit-section', component: EditSection }
];

const router = new VueRouter({
    routes
});

const app = new Vue({
    el: '#app',
    router
});
