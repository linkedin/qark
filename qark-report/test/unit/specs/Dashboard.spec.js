import Vue from 'vue'
import Report from '@/views/Report'

describe('Report', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(Report)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('.text-info').textContent)
      .to.equal('Hello World')
  })
})
