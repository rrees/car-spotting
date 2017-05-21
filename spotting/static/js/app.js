

function readModels(brand) {
	return fetch('/api/brand/' + brand + '/models/suggestions')
				.then((response) => {
					if(response.ok) {
						return response.json()
							.then((json) => {
								//console.log(json);
								return json.models;
							})
					} else {
						return [];
					}
				});
}

function readSubTypes(brand) {
	return fetch('/api/brand/' + brand + '/models/sub-types/suggestions')
				.then((response) => {
					if(response.ok) {
						return response.json()
							.then((json) => {
								//console.log(json);
								return json.models;
							})
					} else {
						return [];
					}
				});
}


const app = new Vue({
	delimiters: ["[[", "]]"],
	el: "#spotting-form",
	data: {
		brand: undefined,
		model: undefined,
		models: undefined,
		brandFree: undefined,
		suggestedBrands: undefined,
		modelSubTypes: undefined,
	},
	methods: {
		setModel: function(modelName) {
			const vm = this;
			vm.model = modelName;
			vm.models = [];
		},
		addSubType: function(subType) {
			const vm = this;
			vm.model = `${vm.model} ${subType}`;
			vm.modelSubTypes = [];
		},
	},
	computed: {
		modelChoicesPresent: function() {
			return this.models.length > 0;
		}
	},
	watch: {
		brand: function() {
			const vm = this;
			const searchBrand = vm.brand.trim();
			readModels(searchBrand).then((models) => vm.models = models);
			readSubTypes(searchBrand).then((subTypes) => vm.modelSubTypes = subTypes);
		},
		brandFree: function() {
			const vm = this;
			const searchBrand = vm.brandFree.trim();
			readModels(searchBrand).then((models) => vm.models = models);
		}
	}
});

