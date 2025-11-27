CREATE OR REPLACE FUNCTION update_member_check_ins()
RETURNS TRIGGER AS $$ BEGIN
    UPDATE members
    SET total_check_ins = total_check_ins + 1
    WHERE id = NEW.member_id;
    RETURN NEW;
END;
 $$ LANGUAGE plpgsql;

CREATE TRIGGER attendance_after_insert
AFTER INSERT ON attendances
FOR EACH ROW
EXECUTE FUNCTION update_member_check_ins();