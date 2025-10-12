
from .dls import run
def run_ids(self, max_depth=50):
    state_count = 0
    step_count = 0
    best_path = []

    for depth in range(1, max_depth + 1):
        # gọi dls với self và depth hiện tại
        path, algo_detail = run(self, limit=depth, original_limit=depth)

        # nếu tìm thấy lời giải → trả về ngay
        if algo_detail and algo_detail.get("solution_found") is True:
            return path, algo_detail

        # nếu chưa có lời giải, cập nhật best path
        elif algo_detail and len(path) > len(best_path):
            best_path = path
            state_count = algo_detail.get("total_states_visited", state_count)
            step_count = algo_detail.get("total_steps_processed", step_count)

    # nếu không tìm thấy lời giải nào → trả về best path tìm được
    return self.save_result(best_path, False, state_count, step_count)
