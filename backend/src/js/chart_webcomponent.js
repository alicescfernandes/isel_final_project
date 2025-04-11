
const API_BASE_URL = 'http://localhost:8000/api/v2/'
class PlotlyChart extends HTMLElement {
    constructor() {
        super();
        this.className = 'col-span-4 p-6 bg-white border border-gray-200 rounded-lg shadow-sm'
        this.id = `chart_${Math.floor(Math.random() * 1e6)}`;
        this.state = {
            chartSlug: this.getAttribute("chart_slug"),
            initialLoad: true,
            quarterNumber: this.getAttribute("q"),
            isError: false,
            isLoading:true
        };

    }

    static get observedAttributes() {
        return ['chart_slug'];
    }

    fetchData() {
        // ?slug=customer_needs_and_wants&quarter=1eac6e9c-f4a3-4d28-b9e5-0837b2e2c0e3`
        const params = new URLSearchParams()

        params.set('slug', this.state.chartSlug)
        params.set('q', this.state.quarterNumber)

        if (this.state.selectedOption) {
            params.set('opt', this.state.selectedOption)
        }

        fetch(`${API_BASE_URL}chart/?${params.toString()}`)
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return res.json()
            })
            .then((data) => {
                const { selected_option, ...rest } = data
                this.setState({
                    initialLoad: false,
                    isLoading: false,
                    selectedOption: Boolean(selected_option) ? selected_option : "", // save what comes from the server
                    ...rest,
                })
            }).catch(() => {
                console.log("setting state", this.state.chartSlug)
                this.setState({
                    initialLoad: false,
                    isLoading:false,
                    isError:true
                })
            })

    }

    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.render()
    }

    renderQuarterNavigation() {
        const select = this.querySelector(`#${this.id} .chart-quarter-navigation`);

        const { quarter } = this.state
        select.innerHTML = `
        <button ${!quarter.prev && 'disabled'} aria-label="Previous Quarter" class="prev-quarter disabled:text-gray-100 text-gray-500 text-xl">←</button>
        <button ${!quarter.next && 'disabled'} aria-label="Next Quarter" class="next-quarter disabled:text-gray-100 text-gray-500 text-xl">→</button>`
    }

    renderSpinner() {
        this.innerHTML = `<div role="status" class="flex justify-center items-center">
                            <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                            </svg>
                            <span class="sr-only">Loading...</span>
                        </div>
                    `
    }

    renderError() {
        this.innerHTML = `
            <div class="flex items-center p-4 mb-4 text-sm text-red-800 border border-red-300 rounded-lg bg-red-50 dark:text-red-400 dark:border-red-800" role="alert">
            <svg class="shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
            </svg>
            <span class="sr-only">Info</span>
            <div>
                <span class="font-bold">Unable to render chart.</span> Try uploading a new one with the data.
            </div>
            </div>
        `;
    }

    renderEmptyState() {
        return `
            <div class="flex items-center p-4 mb-4 text-sm text-blue-800 border border-blue-300 rounded-lg bg-blue-50 dark:text-blue-400 dark:border-blue-800" role="alert">
                <svg class="shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
                </svg>
                <span class="sr-only">Info</span>
                <div>
                    The graph doesn't have data to show.
                </div>
            </div>
        `;
    }
    render() {
        const hasOptions = Boolean(this.state.options && this.state.options.length > 0);


        if (this.state.initialLoad) {
            return this.renderSpinner()
        }

        if(this.state.isError){
            return this.renderError()
        }
    
        this.innerHTML = `<div id="${this.id}"> 
                <div class="chart-header flex justify-between mb-2">
                    <h5 class="chart-title text-2xl font-semibold tracking-tight  flex-1"></h5>
                    <div class="chart-quarter-navigation">
                    </div>
                </div>
                
                ${hasOptions ? `
                    <p> Filter By: 
                    <select class="chart-filter mb-4 p-2 border rounded-md text-sm"></select>
                    </p>` : ''}
                <div class="chart" style="width:100%;height:400px;"></div>
                </div>`;

        this.renderChart();
        this.renderQuarterNavigation()
        if (hasOptions) {
            this.renderOptions();
            this.setupEvents();
        }

    }

    attributeChangedCallback() {
        const hasOptions = Boolean(this.state.option)

        if (hasOptions) {
            this.renderOptions();
            this.setupEvents();
        }

        this.renderChart();
    }

    renderOptions() {
        const select = this.querySelector(`#${this.id} .chart-filter`);
        if (!select) return;

        const { options, selectedOption } = this.state

        select.innerHTML = '';

        for (const opt of options) {
            const optionEl = document.createElement('option');
            optionEl.value = opt;
            optionEl.textContent = opt;
            optionEl.selected = opt === selectedOption;
            select.appendChild(optionEl);
        }
    }

    connectedCallback() {
        this.fetchData()
        this.render()
    }

    setupEvents() {
        const select = this.querySelector(`#${this.id} .chart-filter`);
        if (select) {
            select.addEventListener('change', (e) => {
                const value = e.target.value;
                this.setState({
                    selectedOption: value
                })

                this.fetchData()
            });
        }

        const prev_quarter_btn = this.querySelector(`#${this.id} .prev-quarter`);
        if (prev_quarter_btn) {
            prev_quarter_btn.addEventListener('click', (e) => {
                this.setState({
                    quarterNumber: this.state.quarter.prev
                })

                this.fetchData()
            });
        }

        const next_quarter_btn = this.querySelector(`#${this.id} .next-quarter`);
        if (next_quarter_btn) {
            next_quarter_btn.addEventListener('click', (e) => {
                this.setState({
                    quarterNumber: this.state.quarter.next
                })

                this.fetchData()
            });
        }
    }

    // Chart is fully configured from the backend, using the Plotly API
    async renderChart() {
        
        if (!this.isConnected || this.state.isLoading) return;
        
        const { title, chart_config } = this.state

        const { traces, layout} = chart_config

        const container = this.querySelector(`#${this.id} .chart`);


        const titleEl = this.querySelector(`#${this.id} .chart-title`);
        if (titleEl) titleEl.textContent = `${title} - Q${this.state.quarter.current}`;

        if(traces.length <= 0){
            container.innerHTML = this.renderEmptyState()
            return;
        }

        if (!window.Plotly) {
            await import('https://cdn.plot.ly/plotly-2.30.0.min.js');
        }

        if (container) {
            Plotly.newPlot(container, traces, layout, {
                responsive: true,
            });
        }
    }
}

customElements.define('plotly-chart', PlotlyChart);