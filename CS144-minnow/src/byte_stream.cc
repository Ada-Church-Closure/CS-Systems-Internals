#include "byte_stream.hh"
#include <algorithm>

using namespace std;
// 实现一个可靠的字节流.
ByteStream::ByteStream( uint64_t capacity ) : capacity_( capacity ) {}

bool Writer::is_closed() const
{
  return is_closed_;
}

/**
 * 往deque队列中压入一些数据
 */
void Writer::push( string data )
{
  if(is_closed_ || error_ || data.empty()){
    return;
  }

  const size_t len_to_write = std::min(data.size(), available_capacity());

  if(len_to_write > 0){
    // 根据长度进行写入
    if(len_to_write == data.size()){
      this->buffer_.push_back(data);
    }else{
      this->buffer_.push_back(data.substr(0, len_to_write));
    }

    this->bytes_buffered_ += len_to_write;
    this->pushed_count_ += len_to_write;
  }
  return;
}

void Writer::close()
{
  if(!is_closed_){
    is_closed_ = true;
  }
}

uint64_t Writer::available_capacity() const
{
  return capacity_ - bytes_buffered_;
}

uint64_t Writer::bytes_pushed() const
{
  return pushed_count_;
}

bool Reader::is_finished() const
{
  return this->buffer_.empty() && is_closed_;
}

uint64_t Reader::bytes_popped() const
{
  return popped_count_;
}

string_view Reader::peek() const
{
  if(this->buffer_.empty()){
    return {};
  }

  string_view front_view = this->buffer_.front();
  // 注意前面的偏移量
  return front_view.substr(this->front_view_offset);
}

// 从deque前方弹出字节,能弹出多少的问题
void Reader::pop( uint64_t len )
{
  uint64_t remaining_to_pop = len;

  while(remaining_to_pop > 0 && !buffer_.empty()){
    string& front_view = buffer_.front();

    uint64_t popped_size = std::min(remaining_to_pop, front_view.size() - this->front_view_offset);

    this->popped_count_ += popped_size;
    this->bytes_buffered_ -= popped_size;
    this->front_view_offset += popped_size;
    remaining_to_pop -= popped_size;

    if(this->front_view_offset == front_view.size()){
      front_view_offset = 0;
      this->buffer_.pop_front();
    }
  }

}

uint64_t Reader::bytes_buffered() const
{
  return this->bytes_buffered_;
}
